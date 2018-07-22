import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class UserInterface {
	
	/***Swing Variables Definition***/
	JFrame frame;
	
	JPanel systemUp;
	JPanel systemDown;
	JPanel systemUpRight;
	JPanel mapData;
	JPanel mapWidth;
	JPanel mapLength;
	JPanel mapDataProcess;
	JPanel beacons;
	ArrayList<JPanel> beaconPanelList;
	JPanel beaconsProcess;
	
	MapDrawPanel map;
	
	JButton setMapWL;
	JButton clearMapWL;
	JButton setBeacons;
	JButton clearBeacons;
	JButton runningMode;
	JButton back;
	
	JLabel MapWidthL;
	JLabel MapLengthL;
	ArrayList<JLabel> BeaconX;
	ArrayList<JLabel> BeaconY;
	
	JTextField mapWidthText;
	JTextField mapLengthText;
	ArrayList<JTextField> BeaconXText;
	ArrayList<JTextField> BeaconYText;
	
	String mapName;
	int beaconNum;
	int width = -1;
	int length = -1;
	ArrayList<Integer> xList = new ArrayList<Integer>();
	ArrayList<Integer> yList = new ArrayList<Integer>();
	
	/********************************/
	
	/***Main Function***/
	public static void main(String[] args) {
		UserInterface transponderNavi = new UserInterface();
		//transponderNavi.go();
	}
	/*******************/
	
	
	public void go(String a, int b) {
		
		/***Font, Map and Color***/
		Font buttonFont = new Font("Arial", Font.BOLD,24);
		Font labelFont = new Font("Arial", Font.PLAIN, 24);
		
		int red = 255;
		int green = 128;
		int blue = 51;
		Color background = new Color(red, green, blue);
		
		mapName = a;
		beaconNum = b;
		
		/********************/
		
		/***Frame and Background Settings***/
		frame = new JFrame("Transponder Navigation");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		systemUp = new JPanel();
		systemUp.setBackground(background);
		systemDown = new JPanel();
		systemDown.setBackground(background);
		systemUpRight = new JPanel();
		
		map = new MapDrawPanel();
		
		mapData = new JPanel();
		mapData.setBackground(background);
		mapWidth = new JPanel();
		mapWidth.setBackground(background);
		mapLength = new JPanel();
		mapLength.setBackground(background);
		mapDataProcess = new JPanel();
		mapDataProcess.setBackground(background);
		
		beacons = new JPanel();
		beaconPanelList = new ArrayList <JPanel>();
		for(int i=0; i<beaconNum; i++)
		{
			JPanel beaconPanel = new JPanel();
			beaconPanel.setBackground(background);
			beaconPanelList.add(beaconPanel);
		}
		beaconsProcess = new JPanel();
		beaconsProcess.setBackground(background);
		
		
		/*********************************/
		
		/***Labels Settings***/
		MapWidthL = new JLabel("\nMap Width         ");
		MapWidthL.setFont(labelFont);
		
		MapLengthL = new JLabel("\nMap Length       ");
		MapLengthL.setFont(labelFont);
		
		BeaconX = new ArrayList<JLabel>();
		BeaconY = new ArrayList<JLabel>();
		
		for(int i=0; i<beaconNum; i++)
		{
			JLabel beaconLX;
			if(i<9)
				beaconLX = new JLabel("  Beacon " + (i+1) +"   X");
			else
				beaconLX = new JLabel("Beacon " + (i+1) +"   X");
			beaconLX.setFont(labelFont);
			BeaconX.add(beaconLX);
		}
		
		for(int i=0; i<beaconNum; i++)
		{
			JLabel beaconLY = new JLabel("       Y");
			beaconLY.setFont(labelFont);
			BeaconY.add(beaconLY);
		}
		
		/*******************/
		
		/***Buttons Setting***/
		setMapWL = new JButton("Set");
		setMapWL.setFont(buttonFont);
		setMapWL.addActionListener(new SetMapListener());
		
		clearMapWL = new JButton("Clear");
		clearMapWL.setFont(buttonFont);
		clearMapWL.addActionListener(new ClearMapListener());
		
		setBeacons = new JButton("Set");
		setBeacons.setFont(buttonFont);
		setBeacons.addActionListener(new SetBeaconsListener());
		
		clearBeacons = new JButton("Clear");
		clearBeacons.setFont(buttonFont);
		clearBeacons.addActionListener(new ClearBeaconsListener());
		
		runningMode = new JButton("Enter");
		runningMode.setFont(buttonFont);
		runningMode.addActionListener(new runningModeListener());
		
		back = new JButton("Back");
		back.setFont(buttonFont);
		back.addActionListener(new backListener());
		/**********************/
		
		/***TextField Setting***/
		mapWidthText = new JTextField(10);
		mapLengthText = new JTextField(10);
		BeaconXText = new ArrayList<JTextField>();
		BeaconYText = new ArrayList<JTextField>();
		
		for(int i=0; i<beaconNum; i++)
		{
			JTextField beaconTX = new JTextField(10);
			BeaconXText.add(beaconTX);
		}
		
		for(int i=0; i<beaconNum; i++)
		{
			JTextField beaconTY = new JTextField(10);
			BeaconYText.add(beaconTY);
		}
		/***********************/
		
		/***Swing Layout***/
		frame.getContentPane().add(BorderLayout.CENTER, systemUp);
		frame.getContentPane().add(BorderLayout.SOUTH, systemDown);
		
		systemUp.setLayout(new BorderLayout());
		systemUp.add(BorderLayout.CENTER, map);
		map.setLayout(new BorderLayout());
		
		systemUp.add(BorderLayout.EAST, systemUpRight);
		
		systemUpRight.setLayout(new BorderLayout());
		systemUpRight.add(BorderLayout.NORTH,mapData);
		mapData.setLayout(new GridLayout(3,1,5,5));
		mapData.add(mapLength);
		mapLength.add(MapLengthL);
		mapLength.add(mapLengthText);
		mapData.add(mapWidth);
		mapWidth.add(MapWidthL);
		mapWidth.add(mapWidthText);
		mapData.add(mapDataProcess);
		mapDataProcess.add(setMapWL);
		mapDataProcess.add(clearMapWL);
		
		systemUpRight.add(BorderLayout.CENTER,beacons);
		beacons.setLayout(new GridLayout(beaconNum+1,1,5,0));
		for(int i=0; i<beaconNum; i++)
		{
			beacons.add(beaconPanelList.get(i));
			beaconPanelList.get(i).add(BeaconX.get(i));
			beaconPanelList.get(i).add(BeaconXText.get(i));
			beaconPanelList.get(i).add(BeaconY.get(i));
			beaconPanelList.get(i).add(BeaconYText.get(i));
		}
		beacons.add(beaconsProcess);
		beaconsProcess.add(setBeacons);
		beaconsProcess.add(clearBeacons);
		
		systemDown.setLayout(new GridLayout(1,2,200,0));
		systemDown.add(runningMode);
		systemDown.add(back);
		
		frame.setSize(2000,1000);
		frame.setVisible(true);
		/**********************/
	}
	
		/*** Button Listener Classes Definition ***/
		class SetMapListener implements ActionListener {
			public void actionPerformed(ActionEvent event) {
				try{
					width = Integer.parseInt(mapWidthText.getText());
					length = Integer.parseInt(mapLengthText.getText());
					frame.repaint();
				}
				catch(NumberFormatException error) {
				JOptionPane.showMessageDialog(frame,"Map Width and Length are not integer");
			}
				
			}
		}
		
		class ClearMapListener implements ActionListener {
			public void actionPerformed(ActionEvent event) {
				width = -1;
				length = -1;
				JOptionPane.showMessageDialog(frame,"Width and Length are cleared, please set them again");
				mapWidthText.setText("");
				mapLengthText.setText("");
				frame.repaint();
			}
		}
		
		class SetBeaconsListener implements ActionListener {
			public void actionPerformed(ActionEvent event) {
				int i=0;
				try{
					for(i=0;i<beaconNum;i++)
					{
						xList.add(Integer.parseInt(BeaconXText.get(i).getText()));
						yList.add(Integer.parseInt(BeaconYText.get(i).getText()));
					}
					frame.repaint();
				}
				catch(NumberFormatException error) {
						xList.clear();
						yList.clear();
						JOptionPane.showMessageDialog(frame,"x and y of Beacon " + (i+1) + " are not integer");
					}
			}
		}
		
		class ClearBeaconsListener implements ActionListener {
			public void actionPerformed(ActionEvent event) {
				xList.clear();
				yList.clear();
				JOptionPane.showMessageDialog(frame,"All beacons' position are clear, please set them again");
				for(int i=0;i<beaconNum;i++){
					BeaconXText.get(i).setText("");
					BeaconYText.get(i).setText("");
				}
				frame.repaint();
			}
		}
		
		class runningModeListener implements ActionListener {
			public void actionPerformed(ActionEvent event) {
				
			}
		}
		
		class backListener implements ActionListener {
			public void actionPerformed(ActionEvent event) {
				new LoginPage().go();
				frame.dispose();
			}
		}

	
	/*******************************************/
	
	class MapDrawPanel extends JPanel{
		public void paintComponent(Graphics g){
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
				System.out.println(beaconNum);
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
			
		}
		
	}
}