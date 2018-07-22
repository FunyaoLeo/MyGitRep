 import java.awt.EventQueue;
    import java.awt.Font;
    import java.awt.event.KeyAdapter;
    import java.awt.event.KeyEvent;
    import java.awt.event.MouseAdapter;
    import java.awt.event.MouseEvent;

    import javax.swing.JButton;
    import javax.swing.JFrame;
    import javax.swing.JLabel;
    import javax.swing.JPanel;
    import javax.swing.border.EmptyBorder;

    public class IndexGUI extends JFrame {
        
        private JPanel contentPane;  
        
        private static IndexGUI frame;

        public static void main(String[] args) {
            init();
        }
        public static void init()  
        {
            EventQueue.invokeLater(new Runnable() {
                public void run() {
                    try {
                        frame = new IndexGUI(); 
                        frame.setVisible(true); 
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
        }
        public IndexGUI() {
            setTitle("KnowYou");  
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); 
            
            setBounds(100, 100, 650, 400);
            contentPane = new JPanel(); 
            contentPane.setBorder(new EmptyBorder(5, 5, 5, 5)); 
            setContentPane(contentPane); 
            contentPane.setLayout(null);  

            JLabel lblNewLabel = new JLabel("Welcome to use KnowYou"); 
            lblNewLabel.setBounds(132, 74, 386, 35);
            lblNewLabel.setFont(new Font("黑体", Font.BOLD | Font.ITALIC, 30));
            contentPane.add(lblNewLabel);

            JButton login = new JButton("Login"); 
            
            login.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    event_Login(); 
                }
            });


          
            login.addKeyListener(new KeyAdapter() {
                @Override
                public void keyPressed(KeyEvent e) {
                    if(e.getKeyCode()==KeyEvent.VK_ENTER)
                    {
                        event_Login();
                    }
                }
            });
            login.setBounds(65, 263, 124, 45);
            contentPane.add(login);

            JButton register = new JButton("Sign Up"); 

            
            register.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    event_register(); 
                }
            });

            
            register.addKeyListener(new KeyAdapter() {
                @Override
                public void keyPressed(KeyEvent e) {
                    if(e.getKeyCode()==KeyEvent.VK_ENTER)
                    {
                        event_register();
                    }
                }
            });
            register.setBounds(489, 263, 109, 45);
            contentPane.add(register);

        }

       
        private void event_Login()
        {
            //setVisible(false);
            //new LoginGUI().loginGUI();
        }

        private void event_register()
        {
            //setVisible(false);
            //new RegisterGUI().registerGUI();
        }
    }