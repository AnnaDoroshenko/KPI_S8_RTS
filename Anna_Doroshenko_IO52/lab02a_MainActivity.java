package com.example.lab02a;

import android.content.Intent;
import android.support.design.widget.TextInputLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {
    public static final String EXTRA_X11 = "com.example.lab02.EXTRA_X11";
    public static final String EXTRA_X21 = "com.example.lab02.EXTRA_X21";
    public static final String EXTRA_X12 = "com.example.lab02.EXTRA_X12";
    public static final String EXTRA_X22 = "com.example.lab02.EXTRA_X22";
    public static final String EXTRA_P = "com.example.lab02.EXTRA_P";
    public static final String EXTRA_SIGMA = "com.example.lab02.EXTRA_SIGMA";
    public static final String EXTRA_W1 = "com.example.lab02.EXTRA_W1";
    public static final String EXTRA_W2 = "com.example.lab02.EXTRA_W2";

    private TextInputLayout input_x11_layout, input_x21_layout, input_x12_layout, input_x22_layout,
            input_p_layout, input_sigma_layout, input_w1_layout, input_w2_layout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        input_x11_layout = findViewById(R.id.input_x11_layout);
        input_x21_layout = findViewById(R.id.input_x21_layout);
        input_x12_layout = findViewById(R.id.input_x12_layout);
        input_x22_layout = findViewById(R.id.input_x22_layout);
        input_p_layout = findViewById(R.id.input_p_layout);
        input_sigma_layout = findViewById(R.id.input_sigma_layout);
        input_w1_layout = findViewById(R.id.input_w1_layout);
        input_w2_layout = findViewById(R.id.input_w2_layout);
    }

    private boolean validateX11() {
        String text_input_x11 = input_x11_layout.getEditText().getText().toString().trim();
        if (text_input_x11.isEmpty()) {
            input_x11_layout.setError("This field can not be blank");
            return false;
        } else {
            input_x11_layout.setError(null);
            return true;
        }
    }

    private boolean validateX21() {
        String text_input_x21 = input_x21_layout.getEditText().getText().toString().trim();
        if (text_input_x21.isEmpty()) {
            input_x21_layout.setError("This field can not be blank");
            return false;
        } else {
            input_x21_layout.setError(null);
            return true;
        }
    }

    private boolean validateX12() {
        String text_input_x12 = input_x12_layout.getEditText().getText().toString().trim();
        if (text_input_x12.isEmpty()) {
            input_x12_layout.setError("This field can not be blank");
            return false;
        } else {
            input_x12_layout.setError(null);
            return true;
        }
    }

    private boolean validateX22() {
        String text_input_x22 = input_x22_layout.getEditText().getText().toString().trim();
        if (text_input_x22.isEmpty()) {
            input_x22_layout.setError("This field can not be blank");
            return false;
        } else {
            input_x22_layout.setError(null);
            return true;
        }
    }

    private boolean validateP() {
        String text_input_p = input_p_layout.getEditText().getText().toString().trim();
        if (text_input_p.isEmpty()) {
            input_p_layout.setError("This field can not be blank");
            return false;
        } else {
            input_p_layout.setError(null);
            return true;
        }
    }

    private boolean validateSigma() {
        String text_input_sigma = input_sigma_layout.getEditText().getText().toString().trim();
        if (text_input_sigma.isEmpty()) {
            input_sigma_layout.setError("This field can not be blank");
            return false;
        } else if (Double.parseDouble(input_sigma_layout.getEditText().getText().toString()) > 0.4) {
            input_sigma_layout.setError("Invalid value");
            return false;
        } else {
            input_sigma_layout.setError(null);
            return true;
        }
    }

    private boolean validateW1() {
        String text_input_w1 = input_w1_layout.getEditText().getText().toString().trim();
        if (text_input_w1.isEmpty()) {
            input_w1_layout.setError("This field can not be blank");
            return false;
        } else {
            input_w1_layout.setError(null);
            return true;
        }
    }

    private boolean validateW2() {
        String text_input_w2 = input_w2_layout.getEditText().getText().toString().trim();
        if (text_input_w2.isEmpty()) {
            input_w2_layout.setError("This field can not be blank");
            return false;
        } else {
            input_w2_layout.setError(null);
            return true;
        }
    }

    public void calculate(View view) {
        if (!validateX11() || !validateX21() || !validateX12() || !validateX22() ||
                !validateP() || !validateSigma() || !validateW1() || !validateW2()) {
            return;
        }

        int x11 = Integer.parseInt(input_x11_layout.getEditText().getText().toString());
        int x21 = Integer.parseInt(input_x21_layout.getEditText().getText().toString());
        int x12 = Integer.parseInt(input_x12_layout.getEditText().getText().toString());
        int x22 = Integer.parseInt(input_x22_layout.getEditText().getText().toString());
        int p = Integer.parseInt(input_p_layout.getEditText().getText().toString());
        double sigma = Double.parseDouble(input_sigma_layout.getEditText().getText().toString());
        double w1 = Double.parseDouble(input_w1_layout.getEditText().getText().toString());
        double w2 = Double.parseDouble(input_w2_layout.getEditText().getText().toString());

        Intent intent = new Intent(this, PlotActivity.class);
        intent.putExtra(EXTRA_X11, x11);
        intent.putExtra(EXTRA_X21, x21);
        intent.putExtra(EXTRA_X12, x12);
        intent.putExtra(EXTRA_X22, x22);
        intent.putExtra(EXTRA_P, p);
        intent.putExtra(EXTRA_SIGMA, sigma);
        intent.putExtra(EXTRA_W1, w1);
        intent.putExtra(EXTRA_W2, w2);
        startActivity(intent);
    }
}
