package com.example.lab03a;

import android.support.design.widget.TextInputLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private TextInputLayout inputLayout;
    private TextView outputResult;
    private TextView primeResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        inputLayout = findViewById(R.id.input_layout);
        outputResult = findViewById(R.id.result);
        primeResult = findViewById(R.id.prime_result);
    }

    private boolean validateInput() {
        String input = inputLayout.getEditText().getText().toString().trim();
        if (input.isEmpty()) {
            inputLayout.setError("This field can not be blank");
            String strEmpty = "";
            outputResult.setText(strEmpty);
            primeResult.setText(strEmpty);
            return false;
        } else if (Long.parseLong(input) % 2 == 0) {
            inputLayout.setError("Number must be odd");
            String strEmpty = "";
            outputResult.setText(strEmpty);
            primeResult.setText(strEmpty);
            return false;
        } else {
            inputLayout.setError(null);
            return true;
        }
    }

    public void calculate(View view) {
        if (!validateInput()) {
            return;
        }

        long n = Integer.parseInt(inputLayout.getEditText().getText().toString());
        long[] res = factorizeFermat(n);
        long a = res[0];
        long b = res[1];

        String strResult = String.format("%d, %d", a, b);
        outputResult.setText(strResult);

        if (a == 1 || b == 1) {
            String str = String.format("%d is prime number", n);
            primeResult.setText(str);
        } else {
            String strEmpty = "";
            primeResult.setText(strEmpty);
        }
    }

    boolean isPrimeSquare(long x) {
        return ((long)Math.sqrt(x) * (long)Math.sqrt(x) == x);
    }

    long[] factorizeFermat(long n) {
        long x = (long)Math.sqrt(n) + 1;
        while (!isPrimeSquare(x * x - n)) {
            x++;
        }
        long y = (long)Math.sqrt(x * x - n);

        return new long[]{x + y, x - y};
    }
}
