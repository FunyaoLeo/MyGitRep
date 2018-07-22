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
	JPanel loginDown;
	
	JButton login;
	JButton loginBack;
	
	JLabel username;
	JLabel password;
	JLabel welcome;
	JLabel mapName;
	
	JTextField usernameText;
	JPasswordField passwordText;
	JTextField mapNameText;
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
		int green = 153;
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
		password = new JLabel("Password:");
		password.setFont(loginTextFont);
		welcome = new JLabel("Welcome to use Transponder Navigation", JLabel.CENTER);
		welcome.setFont(loginTextFont);
		mapName = new JLabel("Map Name (please include suffix) :");
		mapName.setFont(loginTextFont);
		
		usernameText = new JTextField(15);
		passwordText = new JPasswordField(15);
		mapNameText = new JTextField(15);

		
		
		/*********************************************/
		
		/***Swing Layout***/
		loginFrame.getContentPane().add(loginPanel);
		
		loginPanel.setLayout(new BorderLayout());
		loginPanel.add(BorderLayout.NORTH, loginUp);
		loginPanel.add(BorderLayout.SOUTH, loginDown);
		
		loginUp.setLayout(new GridLayout(2,1,0,50));
		loginUp.add(welcome);
		loginUp.add(loginMid);
		loginMid.setLayout(new GridLayout(3,1,0,30));
		loginMid.add(loginMidUsername);
		loginMid.add(loginMidPassword);
		loginMid.add(loginMidMapName);
		
		loginMidUsername.setLayout(new GridLayout(1,2,0,0));
		loginMidUsername.add(username);
		loginMidUsername.add(usernameText);
		loginMidPassword.setLayout(new GridLayout(1,2,0,0));
		loginMidPassword.add(password);
		loginMidPassword.add(passwordText);
		loginMidMapName.setLayout(new GridLayout(1,2,0,0));
		loginMidMapName.add(mapName);
		loginMidMapName.add(mapNameText);
		
		loginDown.setLayout(new GridLayout(1,2,100,0));
		loginDown.add(login);
		loginDown.add(loginBack);
		/******************/
		
		loginFrame.setBounds(575,250,850,500);
		loginFrame.setVisible(true);
		
	}
	/*** Button Listener Classes Definition ***/
	class loginListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		boolean id = usernameText.getText().equals("ass");
		boolean passwd = Arrays.equals("hole".toCharArray(),passwordText.getPassword());
		String map;
		
		
		if(id & passwd){
			map = mapNameText.getText();
			if(new File(map).exists()){
				new UserInterface().go(map);
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
	
	class loginBackListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		new WelcomePage().go();
		loginFrame.dispose();
		
		}
	}
	/******************************************/
	
}