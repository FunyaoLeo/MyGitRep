import java.util.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class WelcomePage{
	
	/***Swing Variables Definition***/
	JFrame welcomeFrame;
	
	JPanel welcomeUp;
	JPanel welcomeDown;
	JPanel welcomeUpText;
	
	JButton welcomeLogin;
	JButton welcomeExit;
	
	JLabel sayHi;
	JLabel author;
	JLabel welcomePic;
	/*********************************/
	
	/***Main Function***/
	public static void main(String[] args){
		WelcomePage welcomePage = new WelcomePage();
		welcomePage.go();
	}
	/*******************/
	
	public void go(){
		/***Font, Picture and Color***/
		Font welcomeLabelFont = new Font("Arial", Font.BOLD,40);
		Font welcomeButtonFont = new Font("Arial", Font.BOLD, 24);
		
		int red = 255;
		int green = 128;
		int blue = 51;
		Color welcomeBackground = new Color(red, green, blue);
		
		ImageIcon picture = new ImageIcon("welcome.png");
		/*********************/
		
		/***Frame, Panel, Button and Label***/
		welcomeFrame = new JFrame("Transponder Navigation");
		welcomeFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		welcomeUp = new JPanel();
		welcomeUp.setBackground(welcomeBackground);
		welcomeDown = new JPanel();
		welcomeDown.setBackground(welcomeBackground);
		welcomeUpText = new JPanel();
		welcomeUpText.setBackground(welcomeBackground);
		
		welcomeLogin = new JButton("login");
		welcomeLogin.setFont(welcomeButtonFont);
		welcomeLogin.addActionListener(new welcomeLoginListener());
		welcomeExit = new JButton("Exit");
		welcomeExit.setFont(welcomeButtonFont);
		welcomeExit.addActionListener(new welcomeExitListener());
		
		sayHi = new JLabel("Transponder Navigation", JLabel.CENTER);
		sayHi.setFont(welcomeLabelFont);
		sayHi.setForeground(Color.WHITE);
		author = new JLabel("Presented by Group 3", JLabel.CENTER);
		author.setFont(welcomeLabelFont);
		author.setForeground(Color.WHITE);
		welcomePic = new JLabel(picture);
		/*************************************/
		
		/***Swing Layout***/
		welcomeFrame.getContentPane().add(BorderLayout.CENTER, welcomeUp);
		welcomeFrame.getContentPane().add(BorderLayout.SOUTH, welcomeDown);
		
		welcomeUp.setLayout(new GridLayout(2,1,0,0));
		welcomeUp.add(welcomeUpText);
		welcomeUp.add(welcomePic);
		welcomeUpText.setLayout(new GridLayout(2,1,0,0));
		welcomeUpText.add(sayHi);
		welcomeUpText.add(author);
		welcomeDown.setLayout(new GridLayout(1,2,100,0));
		welcomeDown.add(welcomeLogin);
		welcomeDown.add(welcomeExit);
		
		welcomeFrame.setBounds(675,200,650,600);
		welcomeFrame.setVisible(true);
	}
	
	/*** Button Listener Classes Definition ***/
	class welcomeLoginListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		new LoginPage().go();
		welcomeFrame.dispose();
		}
	}
	
	class welcomeExitListener implements ActionListener {
		public void actionPerformed(ActionEvent event) {
		welcomeFrame.dispose();
		
		}
	}
	/*******************************************/	
	
}
		
	
