package com.vizlore.dimitrije.sensorcollector;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Environment;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;


public class MainActivity extends ActionBarActivity implements SensorEventListener {

    private SensorManager mSensorManager;
    private Sensor mAccelerometar;
    private Sensor mGyroscope;
    private BufferedWriter output_acceleration = null;
    private BufferedWriter output_gyroscope = null;
    private Spinner spinner = null;
    private boolean store = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Button button = (Button) findViewById(R.id.start_button);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                store = !store;
                if (!store)
                    button.setText(R.string.start);
                else
                    button.setText(R.string.stop);
            }
        });

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        mAccelerometar = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        mGyroscope = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);

        mSensorManager.registerListener(this, mAccelerometar, SensorManager.SENSOR_DELAY_GAME);
        mSensorManager.registerListener(this, mGyroscope, SensorManager.SENSOR_DELAY_GAME);

        spinner = (Spinner) findViewById(R.id.spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this, R.array.activity_array, android.R.layout.simple_spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(adapter);

        if (isExternalStorageWritable()) {
            File file_acceleration = new File(getStorageDir("sensor_data"), "acceleration.csv");
            File file_gyroscope = new File(getStorageDir("sensor_data"), "gyroscope.csv");

            try {
                output_acceleration = new BufferedWriter(new FileWriter(file_acceleration, true));
                output_gyroscope = new BufferedWriter(new FileWriter(file_gyroscope, true));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    public boolean isExternalStorageWritable() {
        String state = Environment.getExternalStorageState();
        return Environment.MEDIA_MOUNTED.equals(state);
    }

    public File getStorageDir(String albumName) {
        File file = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_DCIM), albumName);
        if (!file.mkdirs()) {
            Log.e("File", "Directory not created");
        }
        return file;
    }

    @Override

    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        Sensor mySensor = event.sensor;

        if (mySensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            Float x = event.values[0];
            Float y = event.values[1];
            Float z = event.values[2];


            try {
                if (output_acceleration != null && store) {
                    output_acceleration.write(event.timestamp + "," + x.toString() + "," + y.toString() + "," +
                                 z.toString() + "," + spinner.getSelectedItem().toString() + "\n");

                    Log.e("File acceleration", "Written to the file");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        else if (mySensor.getType() == Sensor.TYPE_GYROSCOPE) {

            Float x = event.values[0];
            Float y = event.values[1];
            Float z = event.values[2];

            try {
                if (output_gyroscope != null && store) {
                    output_gyroscope.write(event.timestamp + "," + x.toString() + "," + y.toString() + "," +
                            z.toString() + "," + spinner.getSelectedItem().toString() + "\n");

                    Log.e("File gyroscope", "Written to the file");
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        try {
            if (output_acceleration != null)
                output_acceleration.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
