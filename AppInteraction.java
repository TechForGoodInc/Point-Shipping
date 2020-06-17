package com.emilylouden.com;

import java.io.IOException;
import java.net.ServerSocket;

import javax.swing.JTextArea;

public class AppInteraction {

	ServerSocket server;

	AppInteraction() {
		try {
			server = new ServerSocket(4444);
		} catch (IOException e) {
			System.out.println("Could not listen on port 4444");
			System.exit(-1);
		}
	}

	public Thread getClient() {
		while (true) {
			ClientWorker w;
			try {
				// server.accept returns a client connection
				// text area contains request from client
				JTextArea textArea = new JTextArea();
				w = new ClientWorker(server.accept(), textArea);
				Thread t = new Thread(w);
				t.start();
				return t;
			} catch (IOException e) {
				System.out.println("Accept failed: 4444");
				System.exit(-1);
			}
		}
	}

	protected void finalize() {
		// Objects created in run method are finalized when
		// program terminates and thread exits
		try {
			server.close();
		} catch (IOException e) {
			System.out.println("Could not close socket");
			System.exit(-1);
		}
	}
}
