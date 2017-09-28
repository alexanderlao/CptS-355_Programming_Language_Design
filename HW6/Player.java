package game;

import java.awt.*;

public class Player
{
	private int score;			   //player score
	private int lives;
	private int earnLifeScore;
	private boolean gameover=false;	
	public int scoreConstant = 10; //This constant value is used in score calculation. You don't need to change this.
	
	// statistic variables
    private int mouseClicks;
    private int mouseHits;
    private int mouseMisses;
    private int regularBallHits;
    private int shrinkBallHits;
    private int bounceBallHits;

	public Player(int newLives, int newEarnLifeScore)
	{
		this.score = 0; //initialize the score to 0
		this.lives = newLives;
		this.earnLifeScore = newEarnLifeScore;
	}

	/* get player score*/
	public int getScore ()
	{
		return score;
	}
	
	// getter for the player's lives
	public int getLives ()
	{
		return lives;
	}
	
	// getter for the player's score
	// needed to earn a new life
	public int getEarnLifeScore ()
	{
		return earnLifeScore;
	}
	
	public int getMouseClicks ()
	{
		return mouseClicks;
	}

    public int getMouseHits ()
    {
    	return mouseHits;
    }
    
    public int getMouseMisses ()
    {
    	return mouseMisses;
    }
    
    public int getRegularBallHits ()
    {
    	return regularBallHits;
    }
    
    public int getShrinkBallHits ()
    {
    	return shrinkBallHits;
    }
    
    public int getBounceBallHits ()
    {
    	return bounceBallHits;
    }
    
    // setters
    public void setMouseClicks (int newMouseClicks)
	{
		mouseClicks = newMouseClicks;
	}

    public void setMouseHits (int newMouseHits)
    {
    	mouseHits = newMouseHits;
    }
    
    public void setMouseMisses (int newMouseMisses)
    {
    	mouseMisses = newMouseMisses;
    }
    
    public void setRegularBallHits (int newRegularBallHits)
    {
    	regularBallHits = newRegularBallHits;
    }
    
    public void setShrinkBallHits (int newShrinkBallHits)
    {
    	shrinkBallHits = newShrinkBallHits;
    }
    
    public void setBounceBallHits (int newBounceBallHits)
    {
    	bounceBallHits = newBounceBallHits;
    }

	/*check if the game is over*/
	public boolean isGameOver ()
	{
		return gameover;
	}

	/*update player score*/
	public void addScore (int plus)
	{
		score += plus;
	}
	
	public void addClick ()
	{
		mouseClicks += 1;
	}
	
	public void addHit ()
	{
		mouseHits += 1;
	}
	
	public void addMiss ()
	{
		mouseMisses += 1;
	}
	
	public void addRegular ()
	{
		regularBallHits += 1;
	}
	
	public void addShrink ()
	{
		shrinkBallHits += 1;
	}
	
	public void addBounce ()
	{
		bounceBallHits += 1;
	}
	
	// add a life
	public void addLife ()
	{
		lives += 1;
	}
	
	// subtract a life
	public void decreaseLife ()
	{
		lives -= 1;
	}
	
	/*update "game over" status*/
	public void gameIsOver ()
	{
		gameover = true;
	}
	
	public void displayStatistics (Graphics g)
	{
		double hitPercent = 0;
		double missPercent = 0;
		
		// calculate the hit and miss percentages
		if (mouseClicks != 0)
		{
			hitPercent = (mouseHits * 100) / mouseClicks;
			missPercent = 100 - hitPercent;
		}
		
		g.drawString ("Mouse clicks: " + mouseClicks, 100, 210);
		g.drawString ("Mouse hits: " + hitPercent + "%", 100, 230);
		g.drawString ("Mouse misses: " + missPercent + "%", 100, 250);
		g.drawString ("Regular ball hits: " + regularBallHits, 100, 270);
		g.drawString ("Shrink ball hits: " + shrinkBallHits, 100, 290);
		g.drawString ("Bounce ball hits: " + bounceBallHits, 100, 310);
	}
}