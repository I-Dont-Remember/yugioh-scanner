import argparse
import csv
import os
import tcgplayer
import creds


def verify_number(num):
    # can vary in size on both sides of dash
    parts = num.split("-")
    if len(parts) != 2:
        return False
    return True

# TODO: what if we find wrong card? what should we do?
def get_pricing_data(cn, tp):
    names = {}
    results = tp.search(cn)
    details = tp.get_product_details(results)
    # map the id to the name
    for d in details:
        names[d["productId"]] = d["name"]
    print("    Found -> %s" % str(names))
    prices = tp.get_product_pricing(results)
    # format the prices
    prices = [x for x in prices if x["marketPrice"] is not None]
    # add name & card number to listing
    for p in prices:
        p["name"] = names[p["productId"]]
        p["cardNumber"] = cn
        del p["directLowPrice"]
    return prices


def input_loop(writer, tp):
    print("[*] please input one card at a time, [q] to Exit:")
    count = 0
    while True:
        card_number = input("> ")
        if verify_number(card_number):
            data = get_pricing_data(card_number, tp)
            writer.writerows(data)
            count += 1
        else:
            if card_number == "q" or card_number == "Q":
                print("Quit selected after %d cards" % count)
                break
            # TODO: allow user to insert row marking prev row as incorrect?
            print("[!] Yu-Gi-Oh card numbers have two parts divided by a dash")


def file_loop(file_path, tp):
    data = []
    # TODO: verify file is real
    with open(file_path) as f:
        for line in f:
            if verify_number(line):
                print(line)
                data += get_pricing_data(line, tp)
            else:
                print("Not a valid card number -%s" % line)
    return data


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
        # assume user loop if path isn't provided
        if args.path:
            data = file_loop(args.path, tp)
            writer.writerows(data)
        else:
            # use single row at a time versus saving for the end 
            # so if something happens user doesn't lose all their progress
            input_loop(writer, tp)

        print("Wrote output to %s" % output_file)

if __name__ == "__main__":
    main()
