package com.example.lab02a;

import android.content.Intent;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.series.PointsGraphSeries;

public class PlotActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_plot);

        Intent intent = getIntent();
        int x11 = intent.getIntExtra(MainActivity.EXTRA_X11, 0);
        int x21 = intent.getIntExtra(MainActivity.EXTRA_X21, 0);
        int x12 = intent.getIntExtra(MainActivity.EXTRA_X12, 0);
        int x22 = intent.getIntExtra(MainActivity.EXTRA_X22, 0);
        int p = intent.getIntExtra(MainActivity.EXTRA_P, 0);
        double sigma = intent.getDoubleExtra(MainActivity.EXTRA_SIGMA, 0);
        double w1 = intent.getDoubleExtra(MainActivity.EXTRA_W1, 0);
        double w2 = intent.getDoubleExtra(MainActivity.EXTRA_W2, 0);

        double[] res = findCoeff(x11, x21, x12, x22, p, sigma, w1, w2);
        double output_w1 = res[0];
        double output_w2 = res[1];

        GraphView graph = findViewById(R.id.graph);

        if (output_w1 != -1 && output_w2 != -1) {
            TextView textView_w1 = findViewById(R.id.output_w1);
            TextView textView_w2 = findViewById(R.id.output_w2);

            String string_w1 = String.format("%s = %.3f", "w1", output_w1);
            String string_w2 = String.format("%s = %.3f", "w2", output_w2);
            textView_w1.setText(string_w1);
            textView_w2.setText(string_w2);

            graph.getViewport().setXAxisBoundsManual(true);
            graph.getViewport().setMinX(-5);
            graph.getViewport().setMaxX(10);
            graph.getViewport().setYAxisBoundsManual(true);
            graph.getViewport().setMinY(-5);
            graph.getViewport().setMaxY(10);

            graph.getGridLabelRenderer().setNumHorizontalLabels(16);
            graph.getGridLabelRenderer().setNumVerticalLabels(16);

            LineGraphSeries<DataPoint> series = new LineGraphSeries<>();

            for(double x1 = -5; x1 < 10; x1+=0.1) {
                double x2 = (p - x1 * output_w1) / output_w2;
                series.appendData(new DataPoint(x1, x2), true, 150);
            }
            graph.addSeries(series);

            int[] dot1 = {x11, x21};
            int[] dot2 = {x12, x22};
            if  (x12 < x11) {
                dot1[0] = x12;
                dot1[1] = x22;
                dot2[0] = x11;
                dot2[1] = x21;
            }

            PointsGraphSeries<DataPoint> dots = new PointsGraphSeries<>(new DataPoint[] {
                        new DataPoint(dot1[0], dot1[1]),
                        new DataPoint(dot2[0], dot2[1])
            });
            graph.addSeries(dots);
            dots.setShape(PointsGraphSeries.Shape.POINT);
            dots.setSize(10);
            dots.setColor(Color.MAGENTA);
        } else {
            TextView text_res = findViewById(R.id.result_text);
            text_res.setText("Too many iterations");
            text_res.setTextColor(Color.RED);
        }
    }

    public double[] findCoeff(int x11, int x21, int x12, int x22, int p, double sigma, double w1, double w2) {
        int num = 0;
        int isFound = 0;
        int x1, x2;
        int compNum;
        double y;
        double delta;
        int i = 0;
        while(isFound != 2){
            if(num % 2 == 0) {
                x1 = x11;
                x2 = x21;
                compNum = 1;
            } else {
                x1 = x12;
                x2 = x22;
                compNum = 2;
            }
            y = x1 * w1 + x2 * w2;
            delta = p - y;
            if (compare(y, p, compNum)) {
                isFound++;
            } else {
                w1 = w1 + delta * x1 * sigma;
                w2 = w2 + delta * x2 * sigma;
                isFound = 0;
            }
            num++;
            i++;
            if (i > 1000) {
                return new double[]{-1, -1};
            }
        }

        return new double[]{w1, w2};
    }

    public boolean compare(double y, int p, int compNum) {
        return (compNum == 1) ? (y > p) : (y < p);
    }
}
