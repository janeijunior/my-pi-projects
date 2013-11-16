package br.edu.unoesc;

import android.os.Bundle;
import android.app.ActivityGroup;
import android.content.Intent;
import android.content.res.Resources;
import android.widget.TabHost;

@SuppressWarnings("deprecation")
public class MenuPrincipal extends ActivityGroup {
	static TabHost tabHost;
	static int tab = -1;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.menu_principal);
		
		Resources res = getResources();
		tabHost = (TabHost)findViewById(R.id.TabHost1);
		tabHost.setup(this.getLocalActivityManager());
		TabHost.TabSpec spec;
		Intent intent;
		 
		// Adiciona Tab #1
		intent = new Intent().setClass(this, ControleReles.class);
		spec = tabHost.newTabSpec("0").setIndicator("Relês", res.getDrawable(R.drawable.reles)).setContent(intent);
		tabHost.addTab(spec);
		
		// Adiciona Tab #2
		intent = new Intent().setClass(this, ControleAlarme.class);
		spec = tabHost.newTabSpec("0").setIndicator("Alarme", res.getDrawable(R.drawable.alarme)).setContent(intent);
		tabHost.addTab(spec);
				
		// Adiciona Tab #3
		intent = new Intent().setClass(this, VisualizacaoCamera.class);
		spec = tabHost.newTabSpec("0").setIndicator("Câmeras", res.getDrawable(R.drawable.camera)).setContent(intent);
		tabHost.addTab(spec);
		
		// Adiciona Tab #4
		intent = new Intent().setClass(this, ControleAgendamento.class);
		spec = tabHost.newTabSpec("0").setIndicator("Agendamento", res.getDrawable(R.drawable.agendamento)).setContent(intent);
		tabHost.addTab(spec);
		
		//tabHost.setCurrentTab(0);
		
	}
}
