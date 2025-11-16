def nic_banner():
    # Display NIC in fancy ASCII art style
    nic_art = [
        "",
        " ███╗   ██╗ ██╗  ██████╗",
        " ████╗  ██║ ██║ ██╔════╝",
        " ██╔██╗ ██║ ██║ ██║     ",
        " ██║╚██╗██║ ██║ ██║     ",
        " ██║ ╚████║ ██║ ╚██████╗",
        " ╚═╝  ╚═══╝ ╚═╝  ╚═════╝"
    ]

    for line in nic_art:
        print(line)

    print("=" * 25)