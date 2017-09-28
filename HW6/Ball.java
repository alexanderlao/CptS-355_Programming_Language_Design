package game;
import java.applet.*;
import java.awt.*;
import java.util.*;
import java.net.*;
import java.lang.*;

public class Ball
{
    /*Properties of the basic ball. These are initialized in the constructor using the values read from the config.xml file*/
	private int pos_x;			
	private int pos_y; 				
	private int radius;
	private int first_x;			
	private int first_y;					
	private int x_speed;			
	private int y_speed;			
	private int maxspeed;
	Color color;
	AudioClip outSound;
	
    GameWindow gameW;
	Player player;
	
	/*constructor*/
	public Ball (int radius, int initXpos, int initYpos, int speedX, int speedY, int maxBallSpeed, Color color, AudioClip outSound, Player player,  GameWindow gameW)
	{	
		this.radius = radius;

		pos_x = initXpos;
		pos_y = initYpos;

		first_x = initXpos;
		first_y = initYpos;

		x_speed = speedX;
		y_speed = speedY;

		maxspeed = maxBallSpeed;

		this.color = color;

		this.outSound = outSound;

		this.player = player;
		this.gameW = gameW;
	}
	
	// getter
	public int getPosX ()
	{
		return pos_x;
	}
	
	public int getPosY ()
	{
		return pos_y;
	}
	
	public int getRadius ()
	{
		return radius;
	}
	
	public int getXSpeed ()
	{
		return x_speed;
	}
	
	public int getYSpeed ()
	{
		return y_speed;
	}
	
	// setter
	public void setPosX (int newPosX)
	{
		pos_x = newPosX;
	}
	
	public void setPosY (int newPosY)
	{
		pos_y = newPosY;
	}
	
	public void setRadius (int newRadius)
	{
		radius = newRadius;
	}
	
	public void setXSpeed (int newXSpeed)
	{
		x_speed = newXSpeed;
	}
	
	public void setYSpeed (int newYSpeed)
	{
		y_speed = newYSpeed;
	}

	/*update ball's location based on it's speed*/
	public void move ()
	{
		pos_x += x_speed;
		pos_y += y_speed;
	}

	/*when the ball is hit, reset the ball location to its initial starting location*/
	public void ballWasHit ()
	{		
		resetBallPosition();
	}

	/*check whether the player hit the ball. If so, update the player score based on the current ball speed. */	
	public boolean userHit (int maus_x, int maus_y)
	{	
		double x = maus_x - pos_x;
		double y = maus_y - pos_y;

		double distance = Math.sqrt ((x*x) + (y*y));
		
		if (distance-this.radius < (int)(player.scoreConstant)) 
		{
			player.addScore (player.scoreConstant * Math.abs(x_speed) + player.scoreConstant);
			return true;
		}
		else return false;
	}

    // reset the ball position to its initial starting location
	// and change its speed
	public void resetBallPosition()
	{
		// reset the ball to its initial starting position
		pos_x = first_x;
		pos_y = first_y;
		
		// generate a new random speed up to the maxspeed
		// the range of the random speed is [-maxspeed, maxspeed]
		Random newRandom = new Random ();
		int randomSpeedX = newRandom.nextInt(maxspeed + maxspeed) - maxspeed;
		int randomSpeedY = newRandom.nextInt(maxspeed + maxspeed) - maxspeed;
		
		// the speed should not be zero, so we add one
		if (randomSpeedX == 0)
		{
			randomSpeedX += 1;
		}
		
		if (randomSpeedY == 0)
		{
			randomSpeedY += 1;
		}
		
		// set the speed to the new random speed
		// that we generated
		x_speed = randomSpeedX;
		y_speed = randomSpeedY;
	}
	
	/*check if the ball is out of the game borders. if so, game is over!*/ 
	public boolean isOut ()
	{
		if ((pos_x < gameW.x_leftout) || (pos_x > gameW.x_rightout) || (pos_y < gameW.y_upout) || (pos_y > gameW.y_downout)) 
		{	
			resetBallPosition();	
			outSound.play();
		
			return true;
		}	
		else return false;
	}

	/*draw ball*/
	public void DrawBall (Graphics g)
	{
		g.setColor (color);
		g.fillOval (pos_x - radius, pos_y - radius, 2 * radius, 2 * radius);
	}
}