package game;
import java.awt.*;
import java.util.*;
import java.applet.*;
import java.net.*;
import java.text.Format.Field;
import java.awt.event.MouseEvent;
import java.io.File;

import javax.swing.event.*;
/*<applet code="Main" height=400 width=400></applet>*/
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

public class Main extends Applet implements Runnable
{					
    private int numBalls;						// initialized with the value in the XML file

    private int refreshrate = 15;	           //Refresh rate for the applet screen. Do not change this value. 
	private boolean isStoped = true;		     
    Font f = new Font ("Arial", Font.BOLD, 18);
	
	private Player player;			           //Player instance.		
	private Ball[] ballList = new Ball[10];    //Ball instance. You need to replace this with an array of balls.     
	Thread th;						           //The applet thread. 

	AudioClip shotnoise;	
	AudioClip hitnoise;		
	AudioClip outnoise;		
	  
    Cursor c;				
    private GameWindow gwindow;                 // Defines the borders of the applet screen. A ball is considered "out" when it moves out of these borders.
	private Image dbImage;
	private Graphics dbg;

	
	class HandleMouse extends MouseInputAdapter 
	{
    	public HandleMouse() 
    	{
            addMouseListener(this);
        }
		
    	public void mouseClicked(MouseEvent e) 
    	{
        	if (!isStoped) 
        	{
        		// add another mouse click
        		player.addClick();
        		
        		// loop through each ball
				for (int i = 0; i < numBalls; i++)
				{
					// check if they were hit
					if (ballList[i].userHit (e.getX(), e.getY())) 
					{
		        		hitnoise.play();
		        		
		        		ballList[i].ballWasHit ();
		        		
		        		// check which ball was hit and add to its number of hits
		        		if (ballList[i] instanceof Ball)
		        		{
		        			player.addRegular();
		        		}
		        		if (ballList[i] instanceof ShrinkBall)
		        		{
		        			player.addShrink();
		        		}
		        		if (ballList[i] instanceof BounceBall)
		        		{
		        			player.addBounce();
		        		}
		        		
		        		// update the score
		        		player.addScore(player.scoreConstant);
		        		
		        		// add another mouse hit
		        		player.addHit();
		        		
		        		// check if we need to add a life
		        		if (player.getScore() % player.getEarnLifeScore () == 0)
		        		{
		        			player.addLife();
		        		}
		        	}
					else 
					{	
						shotnoise.play();
					}
				}
			}
			else if (isStoped && e.getClickCount() == 2) 
			{
				isStoped = false;
				init ();
			}
    	}

    	public void mouseReleased(MouseEvent e) 
    	{
           
    	}
        
    	public void RegisterHandler() 
    	{

    	}
    }
	
    /*initialize the game*/
	public void init ()
	{	
		// parse the xml file
		// code adapted from: https://www.mkyong.com/java/how-to-read-xml-file-in-java-dom-parser/
		try 
	    {
			File xmlFile = new File("C:\\Users\\Alex\\Desktop\\HW6\\config2.xml");
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(xmlFile);
	
			//optional, but recommended
			//read this - http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
			doc.getDocumentElement().normalize();
	
			System.out.println("Root element : " + doc.getDocumentElement().getNodeName());
	
			// parsing and initializing the balls
			NodeList nList = doc.getElementsByTagName("Ball");
			numBalls = nList.getLength();
	
			for (int temp = 0; temp < numBalls; temp++) 
			{
				Node nNode = nList.item(temp);
	
				System.out.println("\nCurrent Element : " + nNode.getNodeName());
	
				if (nNode.getNodeType() == Node.ELEMENT_NODE) 
				{
					Element eElement = (Element) nNode;
					
					// convert the read in values to ints
					int tempID = Integer.parseInt(eElement.getAttribute("id"));
					String tempType = eElement.getElementsByTagName("type").item(0).getTextContent();
					int tempRadius = Integer.parseInt(eElement.getElementsByTagName("radius").item(0).getTextContent());
					int tempXPos = Integer.parseInt(eElement.getElementsByTagName("initXpos").item(0).getTextContent());
					int tempYPos = Integer.parseInt(eElement.getElementsByTagName("initYpos").item(0).getTextContent());
					int tempXSpeed = Integer.parseInt(eElement.getElementsByTagName("speedX").item(0).getTextContent());
					int tempYSpeed = Integer.parseInt(eElement.getElementsByTagName("speedY").item(0).getTextContent());
					int tempMaxSpeed = Integer.parseInt(eElement.getElementsByTagName("maxBallSpeed").item(0).getTextContent());
					String stringColor = eElement.getElementsByTagName("color").item(0).getTextContent();
					Color realColor = (Color) Color.class.getField(stringColor).get(null);
					
					//int radius, int initXpos, int initYpos, int speedX, int speedY, int maxBallSpeed, Color color, AudioClip outSound, Player player,  GameWindow gameW
					/* The parameters for the Ball constructor (radius, initXpos, initYpos, speedX, speedY, maxBallSpeed, color) 
					should be initialized with the values read from the config.xml file. Note that the color value need to be converted from String to Color. */
					// call the correct constructor based on the type of ball
					if (tempType.equals("basicball"))
					{
						ballList[temp] = new Ball(tempRadius, tempXPos, tempYPos, tempXSpeed, tempYSpeed, tempMaxSpeed, realColor, outnoise, player, gwindow);
					}
					else if (tempType.equals("shrinkball"))
					{
						ballList[temp] = new ShrinkBall(tempRadius, tempXPos, tempYPos, tempXSpeed, tempYSpeed, tempMaxSpeed, realColor, outnoise, player, gwindow);
					}
					else if (tempType.equals("bounceball"))
					{
						// parse the bounceCount, has to be inside this if-statement because the bounceball type has an extra field in the XML file
						int tempBounceCount = Integer.parseInt(eElement.getElementsByTagName("bounceCount").item(0).getTextContent());
						ballList[temp] = new BounceBall(tempRadius, tempXPos, tempYPos, tempXSpeed, tempYSpeed, tempMaxSpeed, tempBounceCount, realColor, outnoise, player, gwindow);
					}
					
				}
			}
			
			// parsing and initializing the game window
			nList = doc.getElementsByTagName("GameWindow");
			
			for (int temp = 0; temp < nList.getLength(); temp++) 
			{
				Node nNode = nList.item(temp);
				
				System.out.println("\nCurrent Element : " + nNode.getNodeName());
	
				if (nNode.getNodeType() == Node.ELEMENT_NODE) 
				{
					Element eElement = (Element) nNode;
					
					// convert the read in values to ints
					int tempXLeft = Integer.parseInt(eElement.getElementsByTagName("x_leftout").item(0).getTextContent());
					int tempXRight = Integer.parseInt(eElement.getElementsByTagName("x_rightout").item(0).getTextContent());
					int tempYUp = Integer.parseInt(eElement.getElementsByTagName("y_upout").item(0).getTextContent());
					int tempYDown = Integer.parseInt(eElement.getElementsByTagName("y_downout").item(0).getTextContent());
					
					/* The parameters for the GameWindow constructor (x_leftout, x_rightout, y_upout, y_downout) 
					should be initialized with the values read from the config.xml file*/	
					gwindow = new GameWindow(tempXLeft,tempXRight,tempYUp,tempYDown);
					this.setSize(gwindow.x_rightout+30, gwindow.y_downout+30); //set the size of the applet window.
				}
			}
			
			// parsing and initializing the player
			nList = doc.getElementsByTagName("Player");
			
			for (int temp = 0; temp < nList.getLength(); temp++) 
			{
				Node nNode = nList.item(temp);
				
				System.out.println("\nCurrent Element : " + nNode.getNodeName());
	
				if (nNode.getNodeType() == Node.ELEMENT_NODE) 
				{
	
					Element eElement = (Element) nNode;
					
					// convert the read in values to ints
					int tempLives = Integer.parseInt(eElement.getElementsByTagName("numLives").item(0).getTextContent());
					int tempScoreLives = Integer.parseInt(eElement.getElementsByTagName("score2EarnLife").item(0).getTextContent());
					
					player = new Player (tempLives, tempScoreLives);
				}
			}
	    } 
	    catch (Exception e) 
	    {
	    	e.printStackTrace();
	    }
		
		c = new Cursor (Cursor.CROSSHAIR_CURSOR);
		this.setCursor (c);
		HandleMouse hm = new HandleMouse();	
				
        Color superblue = new Color (0, 0, 255);  
		setBackground (Color.black);
		setFont (f);

		if (getParameter ("refreshrate") != null) 
		{
			refreshrate = Integer.parseInt(getParameter("refreshrate"));
		}
		else refreshrate = 15;

		hitnoise = getAudioClip (getCodeBase() , "gun.au");
		hitnoise.play();
		hitnoise.stop();
		shotnoise = getAudioClip (getCodeBase() , "miss.au");
		shotnoise.play();
		shotnoise.stop();
		outnoise = getAudioClip (getCodeBase() , "error.au");
		outnoise.play();
		outnoise.stop();
	}
	
	/*start the applet thread and start animating*/
	public void start ()
	{		
		if (th==null)
		{
			th = new Thread (this);
		}
		th.start ();
	}
	
	/*stop the thread*/
	public void stop ()
	{
		th=null;
	}

	public void run ()
	{	
		/*Lower this thread's priority so it won't interfere with other processing going on*/
		Thread.currentThread().setPriority(Thread.MIN_PRIORITY);

        /*This is the animation loop. It continues until the user stops or closes the applet*/
		while (true) 
		{
			if (!isStoped) 
			{
				// loop through each ball and move them
				// while always checking if the ball is out
				for (int i = 0; i < numBalls; i++)
				{
					ballList[i].move(); 
					if (ballList[i].isOut())
					{
						// decrease the player's number of lives by one
						player.decreaseLife();
						
						// if the player's number of lives in zero
						// the game is over
						if (player.getLives() == 0)
						{
							player.gameIsOver();
						}
					}
				}
			}
            /*Display it*/
			repaint();
            
			try 
			{
				Thread.sleep (refreshrate);
			}
			catch (InterruptedException ex) 
			{
				
			}			
			Thread.currentThread().setPriority(Thread.MAX_PRIORITY);
		}
	}

	public void paint (Graphics g)
	{
		/*if the game is still active draw the ball and display the player's score. If the game is active but stopped, ask player to double click to start the game*/ 
		if (!player.isGameOver()) 
		{
			// draw the player's score and number of lives
			g.setColor (Color.pink);
			g.drawString ("Score: " + player.getScore(), 10, 40);
			g.drawString ("Lives: " + player.getLives(), 10, 60);
			
			// loop through each ball and draw them
			for (int i = 0; i < numBalls; i++)
			{
				ballList[i].DrawBall(g);
			}
			
			if (isStoped) 
			{
				g.setColor (Color.pink);
				g.drawString ("Double click to start the game!", 60, 200);
			}
		}
		/*if the game is over (i.e., the ball is out) display player's score*/
		else 
		{
			g.setColor (Color.cyan);
			
			g.drawString ("Game over!", 130, 100);
			g.drawString ("You scored " + player.getScore() + " Points!", 90, 140);

			if (player.getScore() < 300) g.drawString ("Well, it could be better!", 100, 190);
			else if (player.getScore() < 600 && player.getScore() >= 300) g.drawString ("That was not so bad", 100, 190);
			else if (player.getScore() < 900 && player.getScore() >= 600) g.drawString ("That was really good", 100, 190);
			else if (player.getScore() < 1200 && player.getScore() >= 900) g.drawString ("You seem to be very good!", 90, 190);
			else if (player.getScore() < 1500 && player.getScore() >= 1200) g.drawString ("That was nearly perfect!", 90, 190);
			else if (player.getScore() >= 1500) g.drawString ("You are the Champion!", 100, 190);
			
			// display the player's statistics
			player.displayStatistics(g);

			g.drawString ("Double click to play again!", 85, 350);

			isStoped = true;	
		}
	}

	public void update (Graphics g)
	{
		if (dbImage == null)
		{
			dbImage = createImage (this.getSize().width, this.getSize().height);
			dbg = dbImage.getGraphics ();
		}
		
		dbg.setColor (getBackground ());
		dbg.fillRect (0, 0, this.getSize().width, this.getSize().height);

		dbg.setColor (getForeground());
		paint (dbg);
		
		g.drawImage (dbImage, 0, 0, this);
	}
}