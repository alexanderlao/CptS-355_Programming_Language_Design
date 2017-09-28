package game;

import java.applet.AudioClip;
import java.awt.Color;

public class BounceBall extends Ball
{
	// fields
	private int numBounces;
	private int bounceCount;
		
	// constructor
	public BounceBall (int radius, int initXpos, int initYpos, int speedX, int speedY, int maxBallSpeed, int newBounceCount,
					   Color color, AudioClip outSound, Player player,  GameWindow gameW)
	{
		super (radius, initXpos, initYpos, speedX, speedY, maxBallSpeed, color, outSound, player, gameW);
		numBounces = newBounceCount;
		bounceCount = newBounceCount;
	}
	
	// check if the ball is out of the game borders. if so, keep bouncing
	public boolean isOut ()
	{
		// if there are no bounces left
		if (numBounces == 0) 
		{	
			// reset the ball's position and its number of bounces
			super.resetBallPosition();
			numBounces = bounceCount;
			outSound.play();
		
			return true;
		}
		// if the ball hit the applet border and there are still bounces left
		else if (((getPosX () < gameW.x_leftout) || (getPosX () > gameW.x_rightout) || 
				 (getPosY () < gameW.y_upout) || (getPosY () > gameW.y_downout)) && numBounces > 0)
		{
			// decrement the number of bounces
			numBounces--;
			
			// add the bounce
			// if it hits the left or right side of the applet
			if ((getPosX () < gameW.x_leftout) || (getPosX () > gameW.x_rightout))
			{
				// change the x-direction
				setXSpeed (getXSpeed () * -1);
			}
			// if it hits the top or bottom of the applet
			else if ((getPosY () < gameW.y_upout) || (getPosY () > gameW.y_downout))
			{
				// change the y-direction
				setYSpeed (getYSpeed () * -1);
			}
			
			return false;
		}
		else return false;
	}
}
