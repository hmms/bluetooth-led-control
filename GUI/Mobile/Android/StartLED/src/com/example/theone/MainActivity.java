package com.example.theone;

import android.net.Uri;
import android.os.Bundle;
import android.app.Activity;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.RadioGroup.OnCheckedChangeListener;

public class MainActivity extends Activity {

	Button button;
	private RadioGroup radioModeGroup;
	private RadioButton radioSexButton;
	SeekBar seekbarred;
	SeekBar seekbargreen;
	SeekBar seekbarblue;
	SeekBar seekbardelay;
	TextView valueRed;
	TextView valueGreen;
	TextView valueBlue;
	TextView valueDelay;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        addListenerOnButton();
        seekbarred.setVisibility(View.GONE);
        seekbarblue.setVisibility(View.GONE);
        seekbargreen.setVisibility(View.GONE);
    }
    
    public void addListenerOnButton() {
    	button=(Button) findViewById(R.id.button1);
    	radioModeGroup=(RadioGroup) findViewById(R.id.radioSex);
    	button.setOnClickListener(new OnClickListener() {
			
			public void onClick(View v) {
				// TODO Auto-generated method stub
//				Intent browserIntent = 
//                        new Intent(Intent.ACTION_VIEW, Uri.parse("http://about.me/the1pawan"));
//				startActivity(browserIntent);
				for(int i = 0; i < radioModeGroup.getChildCount(); i++){
				    ((RadioButton)radioModeGroup.getChildAt(i)).setEnabled(true);
				}
			}
		});
    	
    	radioModeGroup.setOnCheckedChangeListener(new OnCheckedChangeListener() {
			
			public void onCheckedChanged(RadioGroup group, int checkedId) {
				// TODO Auto-generated method stub
				if (checkedId==R.id.radioMode0) {
					seekbarred.setVisibility(View.GONE);
			        seekbarblue.setVisibility(View.GONE);
			        seekbargreen.setVisibility(View.GONE);
					Toast.makeText(MainActivity.this,"Mode0", Toast.LENGTH_SHORT).show();
				}
				else if (checkedId==R.id.radioMode1) {
					seekbarred.setVisibility(View.GONE);
			        seekbarblue.setVisibility(View.GONE);
			        seekbargreen.setVisibility(View.GONE);
					Toast.makeText(MainActivity.this,"Mode1", Toast.LENGTH_SHORT).show();
				} 
				else if (checkedId==R.id.radioMode2) {
					seekbarred.setVisibility(View.GONE);
			        seekbarblue.setVisibility(View.GONE);
			        seekbargreen.setVisibility(View.GONE);
					Toast.makeText(MainActivity.this,"Mode2", Toast.LENGTH_SHORT).show();
				}
				else if (checkedId==R.id.radioMode3) {
					Toast.makeText(MainActivity.this,"Mode3", Toast.LENGTH_SHORT).show();
					seekbarred.setVisibility(View.VISIBLE);
			        seekbarblue.setVisibility(View.VISIBLE);
			        seekbargreen.setVisibility(View.VISIBLE);
				}
			}
		});
    	
    	 seekbarred = (SeekBar) findViewById(R.id.seekBarRed);
    	 valueRed=(TextView) findViewById(R.id.textViewRed);
    	 seekbarred.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
    	 
			public void onStopTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onStartTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProgressChanged(SeekBar seekBar, int progress,
					boolean fromUser) {
				// TODO Auto-generated method stub
				valueRed.setText("SeekBar value is "+progress);
			}
		});
    	 
    	 seekbargreen=(SeekBar) findViewById(R.id.seekBarGreen);
    	 valueGreen=(TextView) findViewById(R.id.textViewGreen);
    	 seekbargreen.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
			
			public void onStopTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onStartTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProgressChanged(SeekBar seekBar, int progress,
					boolean fromUser) {
				// TODO Auto-generated method stub
				valueGreen.setText("SeekBar value is "+progress);
			}
		});
    	 
    	 seekbarblue=(SeekBar) findViewById(R.id.seekBarBlue);
    	 valueBlue=(TextView) findViewById(R.id.textViewBlue);
    	 seekbarblue.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
			
			public void onStopTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onStartTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProgressChanged(SeekBar seekBar, int progress,
					boolean fromUser) {
				// TODO Auto-generated method stub
				valueBlue.setText("SeekBar value is "+progress);
			}
		});
    	 
    	 seekbardelay=(SeekBar) findViewById(R.id.seekBarDelay);
    	 valueDelay=(TextView) findViewById(R.id.textViewDelay);
    	 seekbardelay.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
			
			public void onStopTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onStartTrackingTouch(SeekBar seekBar) {
				// TODO Auto-generated method stub
				
			}
			
			public void onProgressChanged(SeekBar seekBar, int progress,
					boolean fromUser) {
				// TODO Auto-generated method stub
				valueDelay.setText("SeekBar value is "+progress);
			}
		});
    }
    
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
}
