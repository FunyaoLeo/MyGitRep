import java.io.*;
import java.net.*;

class JavaServer {
	public static void main(String args[]) throws Exception {
		String fromClient;
		String toClient;
		String[] tokens;
		double i,j;

		ServerSocket server = new ServerSocket(8080);
		System.out.println("wait for connection on port 8080");

		Socket client = server.accept();
		System.out.println("got connection on port 8080");
		BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
		PrintWriter out = new PrintWriter(client.getOutputStream(),true);
		boolean run = true;
		
		while(run) {
			fromClient = in.readLine();
			//tokens = fromClient.split(",");
			//i = Double.parseDouble(tokens[0]);
			//j = Double.parseDouble(tokens[1]);
			System.out.println("received: " + fromClient);
			
				//toClient = "olleH/n";
				//System.out.println("send olleH");
				//out.println(toClient);
				
			}

		
		System.exit(0);
	}
}