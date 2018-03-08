import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.Color;
import java.awt.BasicStroke;

import javax.swing.JFrame;
import javax.swing.JPanel;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class GMaze extends JPanel 
{
    static final int WALL_LEFT = 1;
    static final int WALL_RIGHT= 2;
    static final int WALL_UP   = 4;
    static final int WALL_DOWN = 8;
    
    protected int   m_nrRows;
    protected int   m_nrCols;
    protected int[] m_cells;
    protected int[] m_path;

    public void readMaze(String fname)
    {
	int r, c, id, nrLines;
	String msg;
   
	try
	{
	    Scanner sc = new Scanner(new File(fname));
	    
	    m_nrRows = sc.nextInt();
	    m_nrCols = sc.nextInt();
	    m_cells = new int[m_nrRows * m_nrCols];
	    for(int i = m_nrRows * m_nrCols - 1; i >= 0; --i)
		m_cells[i] = 0;

	    nrLines = sc.nextInt();
	    
	    for(int j = 0; j < nrLines; ++j)
	    {
		r  = sc.nextInt();
		c  = sc.nextInt();
		id = r * m_nrCols + c;
		msg= sc.next();
		for(int i = 0; i < msg.length(); ++i)
		    if(msg.charAt(i) == 'L')
			m_cells[id] |= WALL_LEFT;
		    else if(msg.charAt(i) == 'R')
			m_cells[id] |= WALL_RIGHT;
		    else if(msg.charAt(i) == 'U')
			m_cells[id] |= WALL_UP;
		    else if(msg.charAt(i) == 'D')
			m_cells[id] |= WALL_DOWN;
	    }
	}
	catch(FileNotFoundException e)
	{
	}
	
    }
    

    public void readPath(String fname)
    {
	int r, c, id, nrLines;
	String msg;
	
   
	try
	{
	    Scanner sc = new Scanner(new File(fname));
	    
	    nrLines = sc.nextInt();
	    m_path = new int[nrLines];
	    
	    System.out.println("reading " + nrLines + " lines");
	    
	    
	    for(int j = 0; j < nrLines; ++j)
	    {
		r  = sc.nextInt();
		c  = sc.nextInt();
		m_path[j] = r * m_nrCols + c;
	    }
	}
	catch(FileNotFoundException e)
	{
	}
	
    }
    
    protected int getOffset()
    {
	return 5;
    }
    
      
    protected int getCellWidth()
    {
	return (int) ((getWidth() - 2.0 * getOffset()) / m_nrCols);
    }

    protected int getCellHeight()
    {
	return (int) ((getHeight() - 2.0 * getOffset()) / m_nrRows);
    }
    
    protected void drawMaze(Graphics2D g)
    {
	if(m_cells == null)
	    return;
	
	int w  = getCellWidth();
	int h  = getCellHeight();
	
	g.setColor(Color.BLUE);	
	
	for(int i = 0; i < m_nrRows * m_nrCols; ++i)
	{
	    int r = i / m_nrCols;
	    int c = i % m_nrCols;
	    
	    if((m_cells[i] & WALL_LEFT) != 0)
		g.drawLine(getOffset() + w * c, getOffset() + r * h, getOffset() + w * c, getOffset() + (r + 1) * h);
	    if((m_cells[i] & WALL_RIGHT) != 0)
		g.drawLine(getOffset() + w * (c+1), getOffset() + r * h, getOffset() + w * (c+1), getOffset() + (r + 1) * h);
	    if((m_cells[i] & WALL_UP) != 0)
		g.drawLine(getOffset() + w * c, getOffset() + r * h, getOffset() + w * (c+1), getOffset() + r * h);
	    if((m_cells[i] & WALL_DOWN) != 0)
		g.drawLine(getOffset() + w * c, getOffset() + (r+1) * h, getOffset() + w * (c+1), getOffset() + (r+1) * h);
	}
    }

    
    protected void drawPath(Graphics2D g)
    {
	if(m_path == null)
	    return;
	
	int w  = getCellWidth();
	int h  = getCellHeight();
	
	g.setColor(Color.RED);	
	
	for(int i = 1; i < m_path.length; ++i)
	{
	    int rp = m_path[i - 1] / m_nrCols;
	    int cp = m_path[i - 1] % m_nrCols;
	    int r  = m_path[i] / m_nrCols;
	    int c  = m_path[i] % m_nrCols;
	    
	    g.drawLine(getOffset() + (int) ((cp + 0.5) * w), 
		       getOffset() + (int) ((rp + 0.5) * h), 
		       getOffset() + (int) ((c + 0.5) * w), 
		       getOffset() + (int) ((r + 0.5) * h));
	}
    }

    public void paint(Graphics g) 
    {
	Graphics2D g2 = (Graphics2D)g;
	g2.setStroke(new BasicStroke(3.0f));
	drawMaze(g2);
	drawPath(g2);
    }

    public static void main(String[] args) 
    {      
	GMaze gMaze = new GMaze();
	
	if(args.length > 0)
	    gMaze.readMaze(args[0]);
	if(args.length > 1)
	    gMaze.readPath(args[1]);
	

	JFrame f = new JFrame();
	f.getContentPane().add(gMaze);
	f.setSize(600, 600);
	f.setVisible(true);
	f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    }
}
