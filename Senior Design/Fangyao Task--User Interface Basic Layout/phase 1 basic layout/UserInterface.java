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
	JPanel map;
	JPanel mapData;
	JPanel mapWidth;
	JPanel mapLength;
	JPanel mapDataProcess;
	JPanel beacons;
	JPanel beaconA;
	JPanel beaconB;
	JPanel beaconC;
	JPanel beaconsProcess;
	JPanel resultToBeacons;
	JPanel AngleA;
	JPanel AngleB;
	JPanel AngleC;
	JPanel resultOfCoordinate;
	JPanel Position;
	
	JButton setMapWL;
	JButton clearMapWL;
	JButton setBeacons;
	JButton clearBeacons;
	
	JLabel Playground;
	JLabel MapPic;
	JLabel MapWidthL;
	JLabel MapLengthL;
	JLabel BeaconAX;
	JLabel BeaconBX;
	JLabel BeaconCX;
	JLabel BeaconAY;
	JLabel BeaconBY;
	JLabel BeaconCY;
	JLabel AngleAL;
	JLabel AngleBL;
	JLabel AngleCL;
	JLabel PositionL;
	
	JTextField mapWidthText;
	JTextField mapLengthText;
	JTextField BeaconAXText;
	JTextField BeaconBXText;
	JTextField BeaconCXText;
	JTextField BeaconAYText;
	JTextField BeaconBYText;
	JTextField BeaconCYText;
	JTextField AngleAText;
	JTextField AngleBText;
	JTextField AngleCText;
	JTextField PositionText;
	
	/********************************/
	
	/***Main Function***/
	public static void main(String[] args) {
		UserInterface transponderNavi = new UserInterface();
		transponderNavi.go();
	}
	/*******************/
	
	public void go() {
		/***Font, Map and Color***/
		Font buttonFont = new Font("Arial", Font.BOLD,24);
		Font labelFont = new Font("Arial", Font.PLAIN, 24);
		
		int red = 255;
		int green = 153;
		int blue = 51;
		Color background = new Color(red, green, blue);
		
		ImageIcon image = new ImageIcon("map.jpg");
		
		/********************/
		
		/***Frame and Background Settings***/
		frame = new JFrame("Transponder Navigation");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		systemUp = new JPanel();
		systemUp.setBackground(background);
		systemDown = new JPanel();
		systemUpRight = new JPanel();
		
		map = new JPanel();
		map.setBackground(background);
		mapData = new JPanel();
		mapData.setBackground(background);
		mapWidth = new JPanel();
		mapWidth.setBackground(background);
		mapLength = new JPanel();
		mapLength.setBackground(background);
		mapDataProcess = new JPanel();
		mapDataProcess.setBackground(background);
		
		beacons = new JPanel();
		beaconA = new JPanel();
		beaconA.setBackground(background);
		beaconB = new JPanel();
		beaconB.setBackground(background);
		beaconC = new JPanel();
		beaconC.setBackground(background);
		beaconsProcess = new JPanel();
		beaconsProcess.setBackground(background);
		
		resultToBeacons = new JPanel();
		AngleA = new JPanel();
		AngleB = new JPanel();
		AngleC = new JPanel();
		AngleA.setBackground(background);
		AngleB.setBackground(background);
		AngleC.setBackground(background);
		resultOfCoordinate = new JPanel();
		Position = new JPanel();
		Position.setBackground(background);
		/*********************************/
		
		/***Labels Settings***/
		Playground = new JLabel("Playground", JLabel.CENTER);
		Playground.setFont(labelFont);
		
		MapPic = new JLabel(image);
		
		MapWidthL = new JLabel("\nMap Width         ");
		MapWidthL.setFont(labelFont);
		
		MapLengthL = new JLabel("\nMap Length       ");
		MapLengthL.setFont(labelFont);
		
		BeaconAX = new JLabel("Beacon A   X");
		BeaconAX.setFont(labelFont);
		
		BeaconBX = new JLabel("Beacon B   X");
		BeaconBX.setFont(labelFont);
		
		BeaconCX = new JLabel("Beacon C   X");
		BeaconCX.setFont(labelFont);
		
		BeaconAY = new JLabel("       Y");
		BeaconAY.setFont(labelFont);
		
		BeaconBY = new JLabel("       Y");
		BeaconBY.setFont(labelFont);
		
		BeaconCY = new JLabel("       Y");
		BeaconCY.setFont(labelFont);
		
		AngleAL = new JLabel("\n\nAngle reference to A       ");
		AngleAL.setFont(labelFont);
		
		AngleBL = new JLabel("Angle reference to B       ");
		AngleBL.setFont(labelFont);
		
		AngleCL = new JLabel("Angle reference to C       ");
		AngleCL.setFont(labelFont);
		
		PositionL = new JLabel("Vehicle Position       ", JLabel.CENTER);
		PositionL.setFont(labelFont);
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
		/**********************/
		
		/***TextField Setting***/
		mapWidthText = new JTextField(10);
		mapLengthText = new JTextField(10);
		BeaconAXText = new JTextField(10);
		BeaconBXText = new JTextField(10);
		BeaconCXText = new JTextField(10);
		BeaconAYText = new JTextField(10);
		BeaconBYText = new JTextField(10);
		BeaconCYText = new JTextField(10);
		AngleAText = new JTextField(6);
		AngleBText = new JTextField(6);
		AngleCText = new JTextField(6);
		PositionText = new JTextField(6);
		/***********************/
		
		/***Swing Layout***/
		frame.getContentPane().add(BorderLayout.CENTER, systemUp);
		frame.getContentPane().add(BorderLayout.SOUTH, systemDown);
		
		systemUp.setLayout(new BorderLayout());
		systemUp.add(BorderLayout.CENTER, map);
		map.setLayout(new BorderLayout());
		map.add(Playground, BorderLayout.NORTH);
		map.add(MapPic, BorderLayout.CENTER);
		
		systemUp.add(BorderLayout.EAST, systemUpRight);
		
		systemUpRight.setLayout(new BorderLayout());
		systemUpRight.add(BorderLayout.NORTH,mapData);
		mapData.setLayout(new GridLayout(3,1,5,5));
		mapData.add(mapWidth);
		mapWidth.add(MapWidthL);
		mapWidth.add(mapWidthText);
		mapData.add(mapLength);
		mapLength.add(MapLengthL);
		mapLength.add(mapLengthText);
		mapData.add(mapDataProcess);
		mapDataProcess.add(setMapWL);
		mapDataProcess.add(clearMapWL);
		
		systemUpRight.add(BorderLayout.CENTER,beacons);
		beacons.setLayout(new GridLayout(4,1,5,0));
		beacons.add(beaconA);
		beaconA.add(BeaconAX);
		beaconA.add(BeaconAXText);
		beaconA.add(BeaconAY);
		beaconA.add(BeaconAYText);
		beacons.add(beaconB);
		beaconB.add(BeaconBX);
		beaconB.add(BeaconBXText);
		beaconB.add(BeaconBY);
		beaconB.add(BeaconBYText);
		beacons.add(beaconC);
		beaconC.add(BeaconCX);
		beaconC.add(BeaconCXText);
		beaconC.add(BeaconCY);
		beaconC.add(BeaconCYText);
		beacons.add(beaconsProcess);
		beaconsProcess.add(setBeacons);
		beaconsProcess.add(clearBeacons);
		
		
		systemDown.setLayout(new GridLayout(1,2,0,5));
		systemDown.add(resultToBeacons);
		systemDown.add(resultOfCoordinate);
		
		resultToBeacons.setLayout(new GridLayout(3,1,0,0));
		resultToBeacons.add(AngleA);
		AngleA.add(AngleAL);
		AngleA.add(AngleAText);
		resultToBeacons.add(AngleB);
		AngleB.add(AngleBL);
		AngleB.add(AngleBText);
		resultToBeacons.add(AngleC);
		AngleC.add(AngleCL);
		AngleC.add(AngleCText);
		
		resultOfCoordinate.setLayout(new GridLayout(1,1,5,5));
		resultOfCoordinate.add(Position);
		Position.add(PositionL);
		Position.add(PositionText);
		
		
		frame.setSize(2000,1000);
		frame.setVisible(true);
		/**********************/
	}
	
	/*** Button Listener Classes Definition ***/
	class SetMapListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		
		}
	}
	
	class ClearMapListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		
		}
	}
	
	class SetBeaconsListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		
		}
	}
	
	class ClearBeaconsListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		
		}
	}
}
	/*******************************************/		
	