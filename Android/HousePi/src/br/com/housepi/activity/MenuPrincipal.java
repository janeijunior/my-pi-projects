package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.HashMap;
import android.annotation.SuppressLint;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.support.v4.app.ActionBarDrawerToggle;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;
import br.com.housepi.R;
import br.com.housepi.classes.Funcoes;

@SuppressLint({"ShowToast" })
public class MenuPrincipal extends ActionBarActivity {
	private static final int MENU_ATUALIZAR = 1;
	private static final int MENU_CONFIG = 2;
	
	private Integer posicao;
	
    private DrawerLayout mDrawerLayout;
    private ListView mDrawerList;
    private ActionBarDrawerToggle mDrawerToggle;

    //private CharSequence mDrawerTitle;
    private CharSequence mTitle;
    private String[] mMenu;
      
    private Toast toast;
    private long lastBackPressTime = 0;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {      
        super.onCreate(savedInstanceState);
        setContentView(R.layout.menu_principal);

        //mTitle = mDrawerTitle = getTitle();
        mMenu = getResources().getStringArray(R.array.menu_array);
        mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
        mDrawerList = (ListView) findViewById(R.id.left_drawer);
        
        int[] image = new int[] {R.drawable.ic_action_settings, R.drawable.ic_action_accounts , R.drawable.ic_action_time, 
        		                 R.drawable.ic_action_view_as_list, R.drawable.ic_action_video,  R.drawable.ic_action_play_over_video, 
        		                 R.drawable.ic_action_about};
        
        ArrayList<HashMap<String,String>> listinfo = new ArrayList<HashMap<String, String>>();
        listinfo.clear();
        
        for(int i = 0; i < mMenu.length; i++){
            HashMap<String, String> hm = new HashMap<String, String>();
            hm.put("name", mMenu[i]);
            hm.put("image", Integer.toString(image[i]));
            listinfo.add(hm);
        }

        String[] from = {"image", "name"};
        int[] to = {R.id.img, R.id.txt};
        SimpleAdapter adapter = new SimpleAdapter(getBaseContext(), listinfo, R.layout.drawer_list_item, from, to);
        mDrawerList.setAdapter(adapter);

        mDrawerLayout.setDrawerShadow(R.drawable.drawer_shadow, GravityCompat.START);   
        mDrawerList.setOnItemClickListener(new DrawerItemClickListener());     
        
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setHomeButtonEnabled(true);

        mDrawerToggle = new ActionBarDrawerToggle(
                this,                  
                mDrawerLayout,         
                R.drawable.ic_drawer,  
                R.string.drawer_open,  
                R.string.drawer_close  
                ) {
            public void onDrawerClosed(View view) {
            	getSupportActionBar().setTitle(mTitle);
            	ActivityCompat.invalidateOptionsMenu(MenuPrincipal.this);
            }

            public void onDrawerOpened(View drawerView) {
            	getSupportActionBar().setTitle(mTitle); //mDrawerTitle
            	ActivityCompat.invalidateOptionsMenu(MenuPrincipal.this); 
            }
        };
        mDrawerLayout.setDrawerListener(mDrawerToggle);
        
        if (savedInstanceState == null) {
            selectItem(0);
        }
        
        posicao = Integer.valueOf(Funcoes.carregarDadosComponente("PosicaoMenu", "0", MenuPrincipal.this));
        setTitle(mMenu[posicao]);
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_principal, menu);
        menu.add(0, MENU_ATUALIZAR, 0, "Atualizar");
        menu.add(0, MENU_CONFIG, 0, "Configurações");
        
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
        return super.onPrepareOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (mDrawerToggle.onOptionsItemSelected(item)) {
            return true;
        }
               
        switch (item.getItemId()) {
	        case MENU_ATUALIZAR:
	        	selectItem(posicao);
				break;
	        case MENU_CONFIG:
				startActivity(new Intent(this, Configuracao.class));
				break;
			default:
				break;
		}
        
        return super.onOptionsItemSelected(item);
    }

    private class DrawerItemClickListener implements ListView.OnItemClickListener {
        @Override
        public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
            selectItem(position);
        }
    }

    private void selectItem(int position) {
    	Fragment newFragment;
        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();

        posicao = position;
        
        switch (position) {
        case 0:
            newFragment = ControleRele.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        case 1:
        	newFragment = ControleAlarme.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        case 2:
        	newFragment = ControleAgendamento.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        case 3:
        	newFragment = TemperaturaHumidade.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        case 4:
        	newFragment = VisualizacaoCamera.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        case 5:
        	newFragment = ControleSomAmbiente.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        case 6:
        	newFragment = Sobre.newInstance(this);
            transaction.replace(R.id.content_frame, newFragment);
            transaction.addToBackStack(null);
            transaction.commit();
            break;
        }
        
        Funcoes.salvarDadosComponente("PosicaoMenu", String.valueOf(position), MenuPrincipal.this);
        mDrawerList.setItemChecked(position, true);
        setTitle(mMenu[position]);
        mDrawerLayout.closeDrawer(mDrawerList); 
    }
    
    @Override
    public void onBackPressed() {
    	if (this.lastBackPressTime < System.currentTimeMillis() - 2000) {
    		toast = Toast.makeText(this, "Pressione o botão voltar novamente para desconectar do servidor.", 2000);
    		toast.show();
    		this.lastBackPressTime = System.currentTimeMillis();
    	} else {
    		if (toast != null) {
    			toast.cancel();
    		}
    		Funcoes.salvarDadosComponente("PosicaoMenu", "0", MenuPrincipal.this);
    		finish();
    		System.exit(0);
    	}
    }
    
    @Override
    public void setTitle(CharSequence title) {
        mTitle = title;
        getSupportActionBar().setTitle(mTitle);
    }

    @Override
    protected void onPostCreate(Bundle savedInstanceState) {
        super.onPostCreate(savedInstanceState);
        mDrawerToggle.syncState();
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        mDrawerToggle.onConfigurationChanged(newConfig);
    }
    
    @Override
    protected void onResume() {
    	//Rele ou Camera
    	try {
    		if ((posicao == 0) || (posicao == 4)) {
        		selectItem(posicao);
        	}
		} catch (Exception e) {
		
		}
    	super.onResume();
    }
}