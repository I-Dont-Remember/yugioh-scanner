import argparse
import csv
import os
import tcgplayer
import creds
import inquirer


def verify_number(num):
    # can vary in size on both sides of dash
    parts = num.split("-")
    if len(parts) != 2:
        return False
    return True


def get_pricing_data(cn, tp):
    names = {}
    results = tp.search(cn)
    if not results:
        return None
    details = tp.get_product_details(results)
    # map the id to the name
    for d in details:
        names[d["productId"]] = d["name"]
    prices = tp.get_product_pricing(results)
    # cleanout empty prices
    prices = [x for x in prices if x["marketPrice"] is not None]
    # add name & card number to listing
    for p in prices:
        p["name"] = names[p["productId"]]
        p["cardNumber"] = cn
        del p["directLowPrice"]
    return prices

# returns bool if we wrote to the file
def ask_user_and_write_to_file(writer, pricing_options):
    wrote = False

    if not pricing_options:
        print("[*] found no items for that number...")
        return wrote

    # let user select which subType they have
    question = inquirer.List("cardChoice",
                    message="Select which subType matches your card:",
                    choices=[("%s:%s<($%s)" %(x["name"],x["subTypeName"],x["marketPrice"])) for x in pricing_options] + ["None"],
                    carousel=True)
    answer = inquirer.prompt([question])["cardChoice"]

    if answer == "None":
        print("[*] skipping writing to file..")
    else:
        name, extra = answer.split(":")
        subType = extra.split("<")[0]
        for item in pricing_options:
            if item["subTypeName"] == subType and item["name"] == name:
                wrote = True
                print("      Writing %s, %s" % (name, subType))
                writer.writerow(item)
    return wrote


# TODO: these loops share almost all the same code, could be combined but at the moment not worth the effort
def input_loop(writer, tp):
    print("[*] please input one card at a time, [q] to Exit:")
    count = 0
    while True:
        card_number = input("[%d cards]$ "%count)
        if verify_number(card_number):
            pricing_options = get_pricing_data(card_number, tp)
            if ask_user_and_write_to_file(writer, pricing_options):
                count += 1
        else:
            if card_number == "q" or card_number == "Q":
                print("Quit selected after %d card(s)" % count)
                break
            print("[!] Yu-Gi-Oh card numbers have two parts divided by a dash")


#TODO: see comment above input_loop
def file_loop(file_path, writer, tp):
    # TODO: verify file is real
    count = 0
    with open(file_path) as f:
        for line in f:
            if verify_number(line):
                print("Evaluating %s..." % line)
                pricing_options = get_pricing_data(line, tp)
                if ask_user_and_write_to_file(writer, pricing_options):
                    count += 1
            else:
                print("Not a valid card number -%s" % line)
        print("Finished reading file after %d card(s)" % count)


def main():
    parser = argparse.ArgumentParser(description="Time to D-D-D-Duel.")
    parser.add_argument("--path", help="Input file of card numbers, 1 per line")
    args = parser.parse_args()

    public_key = creds.data["client_id"]
    private_key = creds.data["client_secret"]
    tp = tcgplayer.TCGplayerClient(public_key,private_key)

    output_file = "output.csv"
    with open(output_file, "w") as fp:
        fn = [
            "cardNumber",
            "productId",
            "subTypeName",
            "name",
            "marketPrice",
            "lowPrice",
            "midPrice",
            "highPrice",
            # "directLowPrice"
            ]
        writer = csv.DictWriter(fp, fieldnames=fn)
        writer.writeheader()

        # use single row at a time versus saving for the end 
        # so if something happens user doesn't lose all their progress
        if args.path:
            file_loop(args.path, writer, tp)
        else:
            input_loop(writer, tp)

        print("Wrote output to %s" % output_file)

if __name__ == "__main__":
    main()
