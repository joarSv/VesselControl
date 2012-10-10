package com.dunderklubben.vesselcontrol;

import android.os.Bundle;
import android.preference.EditTextPreference;
import android.preference.PreferenceActivity;
import android.text.InputType;

public class SettingsActivity extends PreferenceActivity  {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        addPreferencesFromResource(R.xml.settings);
        
        //Set input type of the threshold preference to number 
        EditTextPreference pref = (EditTextPreference)findPreference("threshold");
        pref.getEditText().setInputType(InputType.TYPE_CLASS_NUMBER);
    }
}
