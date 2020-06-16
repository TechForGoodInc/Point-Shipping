package com.emilylouden.com;

public class TestSuite {
	public static void main(String[] args) {
		// Insert_Value insert_test = new Insert_Value();
		// insert_test.insert_value(6, "Simpson", "Lisa", "capitalist earth", "i<3sax");

		RetrieveValues retrieve_test = new RetrieveValues();
		String[] output = retrieve_test.retrieve_values();

		for (String str : output) {
			System.out.println(str);
		}

		Password_Validation validation_test = new Password_Validation();
		if (validation_test.check_password(6, "i<3sax")) {
		System.out.println("Validation test successful");
	}
	}
}
