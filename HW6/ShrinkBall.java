package game;

import java.applet.AudioClip;
import java.awt.Color;

//shrink ball sub class
public class ShrinkBall extends Ball
{
	// fields
	private int initialSize;
	private int shrinkAmount;
	private int smallestRadius;
	
	// constructor
	public ShrinkBall (int radius, int initXpos, int initYpos, int speedX, int speedY, int maxBallSpeed, Color color, AudioClip outSound, Player player,  GameWindow gameW)
	{
		super (radius, initXpos, initYpos, speedX, speedY, maxBallSpeed, color, outSound, player, gameW);
		initialSize = radius;
		
		shrinkAmount = (int)((double)radius * 0.3);
		
		// calculate the smallest size the shrink ball can get to
		smallestRadius = radius - (2 * (shrinkAmount));
	}
	
	public void shrink ()
	{
		// once we reach that limit size
		if (getRadius () == smallestRadius)
		{
			// reset the ball
			setRadius (initialSize);
		}
		else
		{
			// otherwise shrink the ball
			int newRadius = getRadius () - shrinkAmount;
			super.setRadius (newRadius);
		}
	}
	
	public void ballWasHit ()
	{		
		shrink ();
		super.ballWasHit();
	}
}
