package br.com.housepi.activity;

import br.com.housepi.R;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.annotation.SuppressLint;
import android.support.v4.app.ActionBarDrawerToggle;
import android.view.Menu;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.widget.DrawerLayout;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;

@SuppressLint("NewApi")
public class MenuPrincipal extends FragmentActivity {
	private static final int MENU_CONFIG = 1;
	
    final String[] menuEntries = {"Relês", "Alarme", "Agendamento", "Temperatura", "Câmera", "Som Ambiente"};
    final String[] fragments = {
            "br.com.housepi.activity.ControleRele",
            "br.com.housepi.activity.ControleAlarme",
            "br.com.housepi.activity.ControleAgendamento",
            "br.com.housepi.activity.TemperaturaHumidade",
            "br.com.housepi.activity.VisualizacaoCamera",
            "br.com.housepi.activity.ControleSomAmbiente"
    };

    private ActionBarDrawerToggle drawerToggle;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.menu_principal);
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(getActionBar().getThemedContext(), android.R.layout.simple_list_item_1, menuEntries);

        final DrawerLayout drawer = (DrawerLayout)findViewById(R.id.drawer_layout);
        final ListView navList = (ListView) findViewById(R.id.drawer);

        getActionBar().setDisplayHomeAsUpEnabled(true);
        getActionBar().setHomeButtonEnabled(true);    
        getActionBar().setTitle(menuEntries[0]);
        
        drawerToggle = new ActionBarDrawerToggle(
                this,
                drawer,
                R.drawable.ic_drawer,
                R.string.drawer_open,
                R.string.drawer_close
        ) {

            public void onDrawerClosed(View view) {

            }

            public void onDrawerOpened(View drawerView) {

            }
        };

        drawer.setDrawerListener(drawerToggle);

        navList.setAdapter(adapter);
        navList.setOnItemClickListener(new OnItemClickListener(){
            @Override
            public void onItemClick(AdapterView<?> parent, View view, final int pos,long id){
                drawer.setDrawerListener( new DrawerLayout.SimpleDrawerListener(){
                
                    @Override
                    public void onDrawerClosed(View drawerView){
                        super.onDrawerClosed(drawerView);
                        getActionBar().setTitle(menuEntries[pos]);
                        FragmentTransaction tx = getSupportFragmentManager().beginTransaction();
                        tx.replace(R.id.main, Fragment.instantiate(MenuPrincipal.this, fragments[pos]));
                        tx.commit();
                    }
                });
                drawer.closeDrawer(navList);
            }
        });
        FragmentTransaction tx = getSupportFragmentManager().beginTransaction();
        tx.replace(R.id.main,Fragment.instantiate(MenuPrincipal.this, fragments[0]));
        tx.commit();
    }


    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);
        drawerToggle.syncState();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        drawerToggle.onConfigurationChanged(newConfig);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (drawerToggle.onOptionsItemSelected(item)) {
            return true;
        }
        
        switch (item.getItemId()) {
		case MENU_CONFIG:
			startActivity(new Intent(this, Configuracao.class));
			break;
		default:
			break;
		}
        return super.onOptionsItemSelected(item);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_principal, menu);
        menu.add(0, MENU_CONFIG, 0, "Configurações");
        return true;
    }
    
    
    
}
