import sys
args = sys.argv[1:]
print(args)
if len(args) < 6:
    print("Insufficient arguments")
    sys.exit(1)

#{"output": "['514', '431', '951', '1014', '0', '1']\n"}
#906|807|1013|612|0|1
