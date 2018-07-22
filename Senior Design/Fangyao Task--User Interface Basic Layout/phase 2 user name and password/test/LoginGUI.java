 import java.awt.EventQueue;
    import java.awt.Font;
    import java.awt.event.KeyAdapter;
    import java.awt.event.KeyEvent;
    import java.awt.event.MouseAdapter;
    import java.awt.event.MouseEvent;

    import javax.swing.JButton;
    import javax.swing.JFrame;
    import javax.swing.JLabel;
    import javax.swing.JOptionPane;
    import javax.swing.JPanel;
    import javax.swing.JPasswordField;
    import javax.swing.JTextField;
    import javax.swing.border.EmptyBorder;

    import com.Joke.util.JDOM;


    public class LoginGUI extends JFrame {
        private static final long serialVersionUID = 4994949944841194839L;
        private JPanel contentPane;  
        private JTextField IDtxt; 
        private JLabel Passwdlabel;
        private JPasswordField passwordField;
        private JButton login;
        private JButton back;

        /**
         * Launch the application.
         * @return 
         */
        public void loginGUI() {
            EventQueue.invokeLater(new Runnable() {
                public void run() {
                    try {
                        LoginGUI frame = new LoginGUI();
                        frame.setVisible(true);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }

        /**
         * Create the frame.
         */
        public LoginGUI() {
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            setBounds(100, 100, 650, 400);
            contentPane = new JPanel();
            contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
            setContentPane(contentPane);
            contentPane.setLayout(null);

            JLabel IDlabel = new JLabel("Please input ID");
            IDlabel.setBounds(68, 170, 91, 39);
            contentPane.add(IDlabel);

            IDtxt = new JTextField();
            IDtxt.setBounds(206, 179, 126, 21);
            contentPane.add(IDtxt);
            IDtxt.setColumns(10);

            Passwdlabel = new JLabel("Please input password");
            Passwdlabel.setBounds(68, 219, 150, 50);
            contentPane.add(Passwdlabel);

            passwordField = new JPasswordField();
            passwordField.setBounds(206, 234, 126, 21);
            contentPane.add(passwordField);

            login = new JButton("login");

          
            login.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {

                    event_login();
                }
            });

          
            login.addKeyListener(new KeyAdapter() {
                public void keyPressed(KeyEvent e)
                {
                    if(e.getKeyCode()==KeyEvent.VK_ENTER)
                    {
                        event_login();
                    }
                }
            });
            login.setBounds(239, 310, 93, 23);
            contentPane.add(login);

           
            back = new JButton("BACK");
            back.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                     IndexGUI.init();
                     setVisible(false);
                }
            });
            back.setBounds(507, 310, 93, 23);
            contentPane.add(back);

            
            JLabel label = new JLabel("Welcome to use KnowYou");
            label.setFont(new Font("Arial", Font.BOLD | Font.ITALIC, 30));
            label.setBounds(142, 54, 386, 35);
            contentPane.add(label);
        }

        
        private void event_login()
        {
            String id=IDtxt.getText(); 
            String passwd=new String(passwordField.getPassword());
            String flag=JDOM.read(id, passwd);
            if(flag.contains("Successful landing"))
            {
                
                String[] bufs=flag.split("/");
                String name=bufs[1];
                
                JOptionPane.showMessageDialog(contentPane, "Welcome:"+name,"Welcome",JOptionPane.PLAIN_MESSAGE);
                UsersGUI.init(name);
                setVisible(false);
            }
           else
           {
     JOptionPane.showMessageDialog(contentPane,flag,"ERROR",JOptionPane.ERROR_MESSAGE);
           }
         }
    }