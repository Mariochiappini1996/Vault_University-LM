package it.uniroma2.ibds.single_server_queue.statistics;

public class Statistics {

    // Statistical counters
    public int numberDelayed;
    public double totalDelay;
    public double areaUnderQ;
    public double areaUnderB;

    public Statistics() {
        this.numberDelayed = 0;
        this.totalDelay = 0;
        this.areaUnderQ = 0;
        this.areaUnderB = 0;
    }

    @Override
    public String toString() {
        return "\tNumber delayed: " + numberDelayed + 
        String.format("\n\tTotal delayed: %.1f \n\tArea under Q: %.1f \n\tArea under B: %.1f \n", totalDelay, areaUnderQ, areaUnderB);
    }

}
