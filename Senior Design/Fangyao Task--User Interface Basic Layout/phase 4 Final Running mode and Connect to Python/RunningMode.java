import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;

public class RunningMode{
	
	/***Swing Variables Definition***/
	static JFrame runningFrame;
	
	JPanel runningUp;
	JPanel runningRight;
	JPanel runningDown;
	JPanel positionInfo;
	JPanel resultToBeacons;
	ArrayList<JPanel> beaconPanelList;
	JPanel resultOfCoordinate;
	
	JButton back;
	
	ArrayList<JLabel> beaconsL;
	JLabel PositionL;
	
	static ArrayList<JTextField> angleText; 
	static JTextField PositionText;
	
	String mapName;
	int beaconNum;
	int width;
	int length;
	static double positionX = 0;
	static double positionY = 0;
	static int X = 0;
	static int Y = 0;
	ArrayList<Integer> xList = new ArrayList<Integer>();
	ArrayList<Integer> yList = new ArrayList<Integer>();
	
	static Socket client;
	static ServerSocket server;
	
	/***********************************/
	
	/***Main Function***/
	public static void main(String[] args){
		/*
		ArrayList<Integer> XList = new ArrayList<Integer>();
		XList.add(200);
		ArrayList<Integer> YList = new ArrayList<Integer>();
		YList.add(200);
		RunningMode transponderNavi = new RunningMode();
		try{
		transponderNavi.go("map.jpg",1,500,1000,XList,YList);
		}
		catch(Exception e) {
						// If it fails, write the error message to screen
						e.printStackTrace(); 
					}
					*/
	}
	/*******************/
	
	public void go(String a, int b, int c, int d,ArrayList<Integer> e, ArrayList<Integer> f)throws Exception{
		
		/***Font, Map and Color***/
		Font buttonFont = new Font("Arial", Font.BOLD,24);
		Font labelFont = new Font("Arial", Font.PLAIN, 24);
		
		int red = 255;
		int green = 128;
		int blue = 51;
		Color background = new Color(red, green, blue);
		
		mapName = a;
		beaconNum = b;
		width = c;
		length = d;
		xList = e;
		yList = f;
		/****************************/
		
		/***Frame and Background Setting***/
		runningFrame = new JFrame("Trasnsponder Navigation");
		runningFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		runningUp = new JPanel();
		runningUp.setBackground(background);
		runningRight = new JPanel();
		runningRight.setBackground(background);
		runningDown = new JPanel();
		runningDown.setBackground(background);
		
		MapDrawPanel map = new MapDrawPanel();
		
		positionInfo = new JPanel();
		positionInfo.setBackground(background);
		resultToBeacons = new JPanel();
		resultToBeacons.setBackground(background);
		beaconPanelList = new ArrayList<JPanel>();
		for(int i=0; i<beaconNum; i++){
			JPanel beaconPanel = new JPanel();
			beaconPanel.setBackground(background);
			beaconPanelList.add(beaconPanel);
		}
		resultOfCoordinate = new JPanel();
		resultOfCoordinate.setBackground(background);
		/***************************************/
		
		
		/***Labels Settings***/
		beaconsL = new ArrayList<JLabel>();
		for(int i=0; i<beaconNum; i++){
			JLabel beacon = new JLabel(" Beacon "+(i+1)+"'s Angle: ");
			beacon.setFont(labelFont);
			beaconsL.add(beacon);
		}
		PositionL = new JLabel("Coordinate Position: ");
		PositionL.setFont(labelFont);
		/***************************************/
		
		/***Button Setting***/
		back = new JButton("Back");
		back.setFont(buttonFont);
		back.addActionListener(new backListener());
		/********************/
		
		/***TextField Setting***/
		angleText = new ArrayList<JTextField>();
		for(int i=0; i<beaconNum; i++){
			JTextField angle = new JTextField(7);
			angleText.add(angle);
		}
		PositionText = new JTextField(10);
		/************************/
		
		/***Swing Layout***/
		runningFrame.getContentPane().add(BorderLayout.CENTER, runningUp);
		runningFrame.getContentPane().add(BorderLayout.SOUTH, runningDown);
		
		runningUp.setLayout(new BorderLayout());
		runningUp.add(BorderLayout.CENTER,map);
		map.setBackground(background);
		runningUp.add(BorderLayout.EAST,runningRight);
		runningRight.setLayout(new GridLayout(beaconNum+1,1,5,0));
		for(int i=0; i<beaconNum; i++){
			runningRight.add(beaconPanelList.get(i));
			beaconPanelList.get(i).add(beaconsL.get(i));
			beaconPanelList.get(i).add(angleText.get(i));
		}
		runningRight.add(resultOfCoordinate);
		resultOfCoordinate.add(PositionL);
		resultOfCoordinate.add(PositionText);
		
		runningDown.setLayout(new GridLayout(1,1,200,0));
		runningDown.add(back);
		runningFrame.setSize(2000,1000);
		runningFrame.setVisible(true);
		/*********************/
	}
	
	/***Button Listener Class Definition***/
	class backListener implements ActionListener{
		public void actionPerformed(ActionEvent event){
			new LoginPage().go();
			try{
				RunningMode.server.close();
				RunningMode.runningFrame.dispose();
			}
			catch(IOException e){
			 System.out.println(e);
			}
		}
	}
	/***************************************/
	
	class MapDrawPanel extends JPanel{
		public void paintComponent(Graphics g){
			
			System.out.println(2);
			
			Image image = new ImageIcon(mapName).getImage();
			int mapPixelWidth = image.getWidth(null);
			int mapPixelHeight = image.getHeight(null);
			g.drawImage(image,(1432-mapPixelWidth)/2,(881-mapPixelHeight)/2,this);
			/******************************x axis*********************************************/
			g.drawLine((1432-mapPixelWidth)/2-20,(881+mapPixelHeight)/2+20,(1432-mapPixelWidth)/2+20,(881+mapPixelHeight)/2+20);
			g.drawLine((1432-mapPixelWidth)/2+20,(881+mapPixelHeight)/2+20,(1432-mapPixelWidth)/2+15,(881+mapPixelHeight)/2+15);
			g.drawLine((1432-mapPixelWidth)/2+20,(881+mapPixelHeight)/2+20,(1432-mapPixelWidth)/2+15,(881+mapPixelHeight)/2+25);
			/*********************************************************************************/
			
			/******************************y axis*********************************************/
			g.drawLine((1432-mapPixelWidth)/2-20,(881+mapPixelHeight)/2+20,(1432-mapPixelWidth)/2-20,(881+mapPixelHeight)/2-20);
			g.drawLine((1432-mapPixelWidth)/2-20,(881+mapPixelHeight)/2-20,(1432-mapPixelWidth)/2-15,(881+mapPixelHeight)/2-15);
			g.drawLine((1432-mapPixelWidth)/2-20,(881+mapPixelHeight)/2-20,(1432-mapPixelWidth)/2-25,(881+mapPixelHeight)/2-15);
			/**********************************************************************************/
			
			/*****************************origin***********************************************/
			g.drawString("(0,0)",(1432-mapPixelWidth)/2-30,(881+mapPixelHeight)/2+30);
			/**********************************************************************************/
			
			if((width != -1)&&(length != -1)&&(xList.size()!=0)&&(yList.size()!=0)){
				for(int i=0; i<beaconNum; i++){
					g.setColor(Color.red);
					/*************** Coordinate Transformation**********************/
					int xbar = (1432-mapPixelWidth)/2+xList.get(i)*mapPixelWidth/length;
					int ybar = (881+mapPixelHeight)/2-yList.get(i)*mapPixelHeight/width;
					/***************************************************************/
					g.fillOval(xbar-15,ybar-15,30,30);
					System.out.println(xbar);
					System.out.println(ybar);
					Font beaconFont = new Font("Arial", Font.PLAIN, 20);
					g.setColor(Color.WHITE);
					g.setFont(beaconFont);
					g.drawString(Integer.toString(i+1),xbar-11,ybar+6);
				}
			}
			
			g.setColor(Color.BLUE);
			X = (1432-mapPixelWidth)/2+(int)positionX*mapPixelWidth/length;
			Y = (881+mapPixelHeight)/2-(int)positionY*mapPixelHeight/width;
			g.fillOval(X-15,Y-15,30,30);
			
		}
			
	}
	
	
}