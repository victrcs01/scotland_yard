from interface.interface_menu import InterfaceMenu

def main() -> None:
    """
    Ponto de entrada principal do aplicativo.

    Cria e executa a interface do menu principal.
    """
    app_menu = InterfaceMenu()
    app_menu.mainloop()

if __name__ == "__main__":
    main()
