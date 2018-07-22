import java.io.*;
import java.net.*;


public class comm implements Runnable{
		public void goCommunication()throws Exception{
			
			/***Communication Part***/
			String fromClient;
			String toClient;
			String[] tokens;
	
			RunningMode.server = new ServerSocket(8080);
			System.out.println("wait for connection on port 8080");
			
			RunningMode.client = RunningMode.server.accept();
			System.out.println("got connection on port 8080");
			BufferedReader in = new BufferedReader(new InputStreamReader(RunningMode.client.getInputStream()));
			PrintWriter out = new PrintWriter(RunningMode.client.getOutputStream(),true);
			boolean run = true;
			while(run) {
				fromClient = in.readLine();
				tokens = fromClient.split(",");
				RunningMode.positionX = Double.parseDouble(tokens[0]);
				RunningMode.positionY = Double.parseDouble(tokens[1]);
				RunningMode.PositionText.setText(tokens[0]+", "+tokens[1]);
				for(int i=0;i<2;i++)
					RunningMode.angleText.get(i).setText(tokens[i+2]);
				System.out.println("received: " + RunningMode.positionX + "," + RunningMode.positionY+ "," + RunningMode.X+ "," + RunningMode.Y);
				//toClient = "olleH/n";
				//System.out.println("send olleH");
				//out.println(toClient);
				RunningMode.runningFrame.repaint();
			}
		}
		
		public void run(){
			try{
				goCommunication();
			}
			catch(Exception e){
				e.printStackTrace();
			}
		}
}
		/****************************/