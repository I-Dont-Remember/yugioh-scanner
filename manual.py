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

def handle_card_number(cn, tp):
    print(cn)
    # make api requests to get the information about this card
    print(tp.search(cn))

def input_loop(writer, tp):
    print("[*] please input one card number at a time and press Enter:")
    count = 0
    while True:
        card_number = input()
        if verify_number(card_number):
            handle_card_number(card_number, tp)
            count += 1
        else:
            if card_number == "q":
                print("Quit selected after %d cards" % count)
                break

            print("[!] Yu-Gi-Oh card numbers have two parts divided by a dash")


def file_loop(file_path, tp):
    # TODO: verify file is real
    with open(file_path) as f:
        for line in f:
            if verify_number(line):
                handle_card_number(line, tp)
            else:
                print("Not a valid card number -%s" % line)

def main():
    parser = argparse.ArgumentParser(description="Time to D-D-D-Duel.")
    parser.add_argument("--path", help="Input file of card numbers, 1 per line")
    args = parser.parse_args()

    public_key = creds.data["client_id"]
    private_key = creds.data["client_secret"]
    tp = tcgplayer.TCGplayerClient(public_key,private_key)

    # assume user loop if path isn't provided
    if args.path:
        file_loop(args.path, tp)
    else:
        output_file = "output.csv"
        with open(output_file, "w") as fp:
            writer = csv.writer(fp)
            input_loop(writer, tp)

if __name__ == "__main__":
    main()
