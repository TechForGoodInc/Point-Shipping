package data;

import java.util.Scanner;

public class MenuClass {

	public static Scanner scan = new Scanner(System.in);

	/**
	 * Prints out a complete list of choice to choose from.
	 */
	public static void menuList() {

		System.out.println("Please SELECT from the MENU below:\n\n");
		System.out.println("1. Check connectivity to DataBase.\n");
		System.out.println("2. Create Table.\n");
		System.out.println("3. Insert Values.\n");
		System.out.println("4. Edit Table's Values.\n");
		System.out.println("5. Delete Table Values.\n\n");
		System.out.println("6. EXIT PROG\n");

	}

	/**
	 * In this method you are able to make choices by input data from keyboard, and
	 * also, you will have the menu display for every choice you make, unless you
	 * input 6 to exit the program.
	 * 
	 * @param args
	 */
	public static void main(String[] args) {
		DataProcess sqlcon = new DataProcess();
		InsertValueIntoPsql inst = new InsertValueIntoPsql();
		EditTable edit = new EditTable();
		TableCreation tbl = new TableCreation();
		DeleteTablesValu dele = new DeleteTablesValu();
		menuList();
		boolean repeat = true;
		while (repeat) {
			repeat = false;

			int option = scan.nextInt();
			switch (option) {

			case 1:
				System.out.println("---Connection Status:---\n");

				sqlcon.connecting();
				repeat = true;
				break;
			case 2:
				System.out.println("----TABLE----\n");
				tbl.makeTable();
				repeat = true;
				break;
			case 3:
				System.out.println("---INSERTION COMPLETE---\n");
				inst.insertValue();
				repeat = true;
				break;
			case 4:
				System.out.println("---CHANGES MADE---\n");
				edit.editTheTabl();
				repeat = true;
				break;
			case 5:
				System.out.println("---DELETION COMPLETED--\n");
				dele.DeleteValues();
				repeat = true;
				break;
			case 6:
				System.out.println("----Bye!-----");
				repeat = false;
			default:
				if (option == 6) {
					repeat = false;
				}

				else {
					menuList();
					repeat = true;
				}

			}
		}

	}

}
