import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.File;

public class LoginPage{
	
	/***Swing Variables Definition***/
	JFrame loginFrame;
	
	JPanel loginPanel;
	JPanel loginUp;
	JPanel loginMid;
	JPanel loginMidUsername;
	JPanel loginMidPassword;
	JPanel loginMidMapName;
	JPanel loginMidNum;
	JPanel loginDown;
	
	JButton login;
	JButton loginBack;
	
	JLabel username;
	JLabel password;
	JLabel welcome;
	JLabel mapName;
	JLabel numOfBeacons;
	
	JTextField usernameText;
	JPasswordField passwordText;
	JTextField mapNameText;
	JTextField numOfBeaconsText;
	/********************************/
	
	/***Main Function***/
	public static void main(String[] args){
		LoginPage loginPage = new LoginPage();
		loginPage.go();
	}
	/********************/
	
	public void go(){
		/***Font and Color***/
		Font loginButtonFont = new Font("Arial", Font.BOLD, 24);
		Font loginTextFont = new Font("Arial", Font.BOLD, 24);
		
		int red = 255;
		int green = 128;
		int blue = 51;
		Color loginBackground = new Color(red, green, blue);
		/*********************/
		
		/***Frame, Panel, Button, Label and Textfield***/
		loginFrame = new JFrame("Transponder Navigation");
		loginFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		loginPanel = new JPanel();
		loginPanel.setBackground(loginBackground);		
		loginUp = new JPanel();
		loginUp.setBackground(loginBackground);
		loginMid = new JPanel();
		loginMid.setBackground(loginBackground);
		loginMidUsername = new JPanel();
		loginMidUsername.setBackground(loginBackground);
		loginMidPassword = new JPanel();
		loginMidPassword.setBackground(loginBackground);
		loginMidMapName = new JPanel();
		loginMidMapName.setBackground(loginBackground);
		loginMidNum = new JPanel();
		loginMidNum.setBackground(loginBackground);
		loginDown = new JPanel();
		loginDown.setBackground(loginBackground);
		
		
		login = new JButton("Start");
		login.setFont(loginButtonFont);
		login.addActionListener(new loginListener());
		loginBack = new JButton("Back");
		loginBack.setFont(loginButtonFont);
		loginBack.addActionListener(new loginBackListener());
		
		username = new JLabel("Username:");
		username.setFont(loginTextFont);
		username.setForeground(Color.WHITE);
		password = new JLabel("Password:");
		password.setFont(loginTextFont);
		password.setForeground(Color.WHITE);
		welcome = new JLabel("Welcome to use Transponder Navigation", JLabel.CENTER);
		welcome.setFont(loginTextFont);
		welcome.setForeground(Color.WHITE);
		mapName = new JLabel("Map Name (please include suffix):");
		mapName.setFont(loginTextFont);
		mapName.setForeground(Color.WHITE);
		numOfBeacons = new JLabel("Number of Beacons (Please input an integer):");
		numOfBeacons.setFont(loginTextFont);
		numOfBeacons.setForeground(Color.WHITE);
		
		usernameText = new JTextField(15);
		usernameText.addKeyListener(new loginKeyListener());
		passwordText = new JPasswordField(15);
		passwordText.addKeyListener(new loginKeyListener());
		mapNameText = new JTextField(15);
		mapNameText.addKeyListener(new loginKeyListener());
		numOfBeaconsText = new JTextField(15);
		numOfBeaconsText.addKeyListener(new loginKeyListener());

		
		
		/*********************************************/
		
		/***Swing Layout***/
		loginFrame.getContentPane().add(loginPanel);
		
		loginPanel.setLayout(new BorderLayout());
		loginPanel.add(BorderLayout.NORTH, loginUp);
		loginPanel.add(BorderLayout.SOUTH, loginDown);
		
		loginUp.setLayout(new GridLayout(2,1,0,0));
		loginUp.add(welcome);
		loginUp.add(loginMid);
		loginMid.setLayout(new GridLayout(4,1,0,30));
		loginMid.add(loginMidUsername);
		loginMid.add(loginMidPassword);
		loginMid.add(loginMidMapName);
		loginMid.add(loginMidNum);
		
		loginMidUsername.setLayout(new GridLayout(1,2,0,0));
		loginMidUsername.add(username);
		loginMidUsername.add(usernameText);
		loginMidPassword.setLayout(new GridLayout(1,2,0,0));
		loginMidPassword.add(password);
		loginMidPassword.add(passwordText);
		loginMidMapName.setLayout(new GridLayout(1,2,0,0));
		loginMidMapName.add(mapName);
		loginMidMapName.add(mapNameText);
		loginMidNum.setLayout(new GridLayout(1,2,0,0));
		loginMidNum.add(numOfBeacons);
		loginMidNum.add(numOfBeaconsText);
		
		loginDown.setLayout(new GridLayout(1,2,100,0));
		loginDown.add(login);
		loginDown.add(loginBack);
		/******************/
		
		loginFrame.setBounds(425,225,1150,550);
		loginFrame.setVisible(true);
		
	}
	/*** Button Listener Classes Definition ***/
	class loginListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			LogIn();
		}
	}
	
	class loginKeyListener implements KeyListener {
		public void keyPressed(KeyEvent e) {
			int key = e.getKeyCode();
			if(key == KeyEvent.VK_ENTER)
			LogIn();
		}
		
		public void keyReleased(KeyEvent e) {
		}
		
		public void keyTyped(KeyEvent e) {
		}
	}
		
	
	class loginBackListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
		new WelcomePage().go();
		loginFrame.dispose();
		
		}
	}
	/******************************************/
	
	public void LogIn(){
		boolean id = usernameText.getText().equals("gopokes");
		boolean passwd = Arrays.equals("osu".toCharArray(),passwordText.getPassword());
		String map;
		int num;
		
		
		if(id & passwd){
			map = mapNameText.getText();
			
			try {
				num = Integer.parseInt(numOfBeaconsText.getText());
			}
			catch(NumberFormatException error) {
				JOptionPane.showMessageDialog(loginFrame,"Beacon number is not an integer");
			}
			num = Integer.parseInt(numOfBeaconsText.getText());
			if(new File(map).exists()){
				new UserInterface().go(map,num);
				loginFrame.dispose();
			}
			else
				JOptionPane.showMessageDialog(loginFrame,"Invalid map name");	
		}
		else{
			JOptionPane.showMessageDialog(loginFrame,"Invalid Combination of Username and Password");
		}
	}
	
}

