package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.List;

import br.com.housepi.R;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.ContentValues;
import android.content.DialogInterface;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.support.v4.view.MenuItemCompat;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;
import android.widget.AdapterView.OnItemClickListener;
import br.com.housepi.classes.Banco;
import br.com.housepi.classes.Funcoes;

@SuppressLint("NewApi")
public class ConfiguracaoConexao extends ActionBarActivity {
	private EditText edtHost;
	private EditText edtPorta;
	private EditText edtDescricao;
	private MenuItem itemInserir;
	private MenuItem itemAlterar;
	private MenuItem itemRemover;
	private MenuItem itemSalvar;
	private MenuItem itemCancelar;
	private ListView listView;
	private CheckBox cbxConectarAutomaticamente;
	private ArrayAdapter<String> adapter;
	private static final int MENU_INSERIR = 1;
	private static final int MENU_ALTERAR = 2;
	private static final int MENU_REMOVER = 3;
	private static final int MENU_SALVAR = 4;	
	private static final int MENU_CANCELAR = 5;	
	private List<String> conexoes = new ArrayList<String>();
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.configuracao_conexao);
	
		edtHost = (EditText) findViewById(R.id.edtHost);
		edtPorta = (EditText) findViewById(R.id.edtPorta);
		edtDescricao = (EditText) findViewById(R.id.edtDescricaoConexao);
		cbxConectarAutomaticamente = (CheckBox) findViewById(R.id.cbxConectarAutomaticamente);
		
		edtHost.setEnabled(false);
		edtPorta.setEnabled(false);
		edtDescricao.setEnabled(false);
		cbxConectarAutomaticamente.setEnabled(false);
		
		listView = (ListView) findViewById(R.id.listConexoes);
		
		adapter = new ArrayAdapter<String>(this, R.layout.linha_list_view_musica, R.id.listNomeMusica, conexoes);

		listView.setAdapter(adapter);
		
		carregarLista();
		
		listView.setOnItemClickListener(new OnItemClickListener() {
			public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
				Funcoes.salvarDadosComponente("ConexaoSelecionada", conexoes.get(position).toString(), getBaseContext());
								
				carregarDadosComponente();
	        }
	    });	
		
		carregarDadosComponente();
	}	

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		itemInserir = menu.add(0, MENU_INSERIR, 0, "Inserir");
		itemAlterar = menu.add(0, MENU_ALTERAR, 0, "Alterar");
		itemRemover = menu.add(0, MENU_REMOVER, 0, "Remover");
		itemSalvar = menu.add(0, MENU_SALVAR, 0, "Salvar");
		itemCancelar = menu.add(0, MENU_CANCELAR, 0, "Calcelar");
		
		if (android.os.Build.VERSION.SDK_INT >= 11) { 
	        itemInserir.setShowAsActionFlags(MenuItemCompat.SHOW_AS_ACTION_ALWAYS | MenuItemCompat.SHOW_AS_ACTION_WITH_TEXT);
	        itemInserir.setIcon(R.drawable.ic_action_new);
		    itemAlterar.setShowAsActionFlags(MenuItemCompat.SHOW_AS_ACTION_ALWAYS | MenuItemCompat.SHOW_AS_ACTION_WITH_TEXT);
	        itemAlterar.setIcon(R.drawable.ic_action_edit);
		    itemRemover.setShowAsActionFlags(MenuItemCompat.SHOW_AS_ACTION_ALWAYS | MenuItemCompat.SHOW_AS_ACTION_WITH_TEXT);
	        itemRemover.setIcon(R.drawable.ic_action_discard);
	        itemSalvar.setShowAsActionFlags(MenuItemCompat.SHOW_AS_ACTION_ALWAYS | MenuItemCompat.SHOW_AS_ACTION_WITH_TEXT);
	        itemSalvar.setIcon(R.drawable.ic_action_accept);
	        itemCancelar.setShowAsActionFlags(MenuItemCompat.SHOW_AS_ACTION_ALWAYS | MenuItemCompat.SHOW_AS_ACTION_WITH_TEXT);
	        itemCancelar.setIcon(R.drawable.ic_action_remove);
		}
		
		itemSalvar.setVisible(false);
		itemCancelar.setVisible(false);		
		
		return true;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case MENU_INSERIR:
			itemInserir.setVisible(false);
			itemAlterar.setVisible(false);
			itemRemover.setVisible(false);
			itemSalvar.setVisible(true);
			itemCancelar.setVisible(true);
			
			edtHost.setEnabled(true);
			edtPorta.setEnabled(true);
			edtDescricao.setEnabled(true);
			cbxConectarAutomaticamente.setEnabled(true);
		
			edtHost.setText("");
			edtPorta.setText("");
			edtDescricao.setText("");
			cbxConectarAutomaticamente.setChecked(false);
		
			break;
		case MENU_ALTERAR:
			if (edtDescricao.getText().toString().equals("")) {
				Toast.makeText(this, "Sem registros para alterar!", Toast.LENGTH_SHORT).show();
			} else {
				itemInserir.setVisible(false);
				itemAlterar.setVisible(false);
				itemRemover.setVisible(false);
				itemSalvar.setVisible(true);
				itemCancelar.setVisible(true);
				
				edtHost.setEnabled(true);
				edtPorta.setEnabled(true);
				edtDescricao.setEnabled(false);
				cbxConectarAutomaticamente.setEnabled(true);
			}
			
			break;
		case MENU_REMOVER:
			if (edtDescricao.getText().toString().equals("")) {
				Toast.makeText(this, "Sem registros para remover!", Toast.LENGTH_SHORT).show();
			} else {
				AlertDialog.Builder builder = new AlertDialog.Builder(this); 
				builder.setTitle("Confirmação"); 
				builder.setMessage("Deseja realmente remover o registro?"); 
				
				builder.setPositiveButton("Sim", new DialogInterface.OnClickListener() { 
					public void onClick(DialogInterface arg0, int arg1) { 
						Banco banco = new Banco(getBaseContext());
						SQLiteDatabase acessaBanco = banco.getWritableDatabase();
						
						acessaBanco.delete("Conexao", "Descricao=?", new String[]{edtDescricao.getText().toString()});
						
						Toast.makeText(getBaseContext(), "Dados excluídos com sucesso!", Toast.LENGTH_SHORT).show();
						
						edtHost.setText("");
						edtPorta.setText("");
						edtDescricao.setText("");
						cbxConectarAutomaticamente.setChecked(false);
						
						Funcoes.salvarDadosComponente("ConexaoSelecionada", "", getBaseContext());
						carregarLista();
					} 
				}); 
				
				builder.setNegativeButton("Não", new DialogInterface.OnClickListener() { 
					public void onClick(DialogInterface arg0, int arg1) { 
				
					} 
				}); 
				
				AlertDialog alerta = builder.create(); 
				alerta.show();
			}
			
			break;
		case MENU_SALVAR:
			//Inserir
			if (edtDescricao.isEnabled()) {
				if ((!edtDescricao.getText().toString().trim().equals("")) && (!edtHost.getText().toString().trim().equals("")) && (!edtPorta.getText().toString().trim().equals(""))) {
					Banco banco = new Banco(getBaseContext());
					SQLiteDatabase acessaBanco = banco.getWritableDatabase();
					
					Cursor c = acessaBanco.query("Conexao", new String[] {"Descricao", "Host", "Porta"}, "Descricao=?", new String[] {edtDescricao.getText().toString()}, null, null, null, null);
					
					if (c.getCount() > 0) {
						Toast.makeText(this, "Já existe uma conexão com esta descrição. Tente uma diferente!", Toast.LENGTH_SHORT).show();
					} else {
						ContentValues valores = new ContentValues();
						valores.put("Descricao", edtDescricao.getText().toString());
						valores.put("Host", edtHost.getText().toString().trim());
						valores.put("Porta", edtPorta.getText().toString().trim());
						
						if (cbxConectarAutomaticamente.isChecked()) {
							valores.put("ConectarAutomaticamente", 1);
						} else {
							valores.put("ConectarAutomaticamente", 0);
						}						
						
						acessaBanco.insert("Conexao", null, valores);
						
						Toast.makeText(getBaseContext(), "Dados gravados com sucesso!", Toast.LENGTH_SHORT).show();
						
						Funcoes.salvarDadosComponente("ConexaoSelecionada", edtDescricao.getText().toString(), getBaseContext());
						
						itemInserir.setVisible(true);
						itemAlterar.setVisible(true);
						itemRemover.setVisible(true);
						itemSalvar.setVisible(false);
						itemCancelar.setVisible(false);
						
						edtHost.setEnabled(false);
						edtPorta.setEnabled(false);
						edtDescricao.setEnabled(false);
						cbxConectarAutomaticamente.setEnabled(false);
					}
				} else {
					Toast.makeText(getBaseContext(), "Preencha todos os campos!", Toast.LENGTH_SHORT).show();
				}
				
			} else { 
			//Alterar
				if ((!edtHost.getText().toString().trim().equals("")) && (!edtPorta.getText().toString().trim().equals(""))) {
					Banco banco = new Banco(getBaseContext());
					SQLiteDatabase acessaBanco = banco.getWritableDatabase();
					ContentValues valores = new ContentValues();
					
					valores.put("Host", edtHost.getText().toString().trim());
					valores.put("Porta", edtPorta.getText().toString().trim());
					
					if (cbxConectarAutomaticamente.isChecked()) {
						valores.put("ConectarAutomaticamente", 1);
					} else {
						valores.put("ConectarAutomaticamente", 0);
					}
					
					acessaBanco.update("Conexao", valores, "Descricao=?", new String[]{edtDescricao.getText().toString()});
					
					Toast.makeText(getBaseContext(), "Dados alterados com sucesso!", Toast.LENGTH_SHORT).show();
					
					itemInserir.setVisible(true);
					itemAlterar.setVisible(true);
					itemRemover.setVisible(true);
					itemSalvar.setVisible(false);
					itemCancelar.setVisible(false);
						
					edtHost.setEnabled(false);
					edtPorta.setEnabled(false);
					edtDescricao.setEnabled(false);
					cbxConectarAutomaticamente.setEnabled(false);
				} else {
					Toast.makeText(getBaseContext(), "Informe o Host e a porta!", Toast.LENGTH_SHORT).show();
				}	
			}
			
			carregarLista();
			
			break;
		case MENU_CANCELAR:
			carregarDadosComponente();
			
			itemInserir.setVisible(true);
			itemAlterar.setVisible(true);
			itemRemover.setVisible(true);
			itemSalvar.setVisible(false);
			itemCancelar.setVisible(false);
			
			edtHost.setEnabled(false);
			edtPorta.setEnabled(false);
			edtDescricao.setEnabled(false);
			cbxConectarAutomaticamente.setEnabled(false);
			
			break;
		default:
			break;
		}
		return true;
	}
		
	private void carregarLista() {
		Banco banco = new Banco(this);
		SQLiteDatabase acessaBanco = banco.getWritableDatabase();
		
		Cursor c = acessaBanco.query("Conexao", new String[]{"Descricao"}, null, null, null, null, null);
		c.moveToFirst();
		
		conexoes.clear();
		
		while (!c.isAfterLast()) {
			conexoes.add(c.getString(0));
			c.moveToNext();
		}
		
		adapter.notifyDataSetChanged();
	}
	
	private void carregarDadosComponente() {
		String descricao = Funcoes.carregarDadosComponente("ConexaoSelecionada", "", this);

		if (!descricao.equals("")) {
			Banco banco = new Banco(getBaseContext());
			SQLiteDatabase acessaBanco = banco.getWritableDatabase();
					
			Cursor c = acessaBanco.query("Conexao", new String[] {"Descricao", "Host", "Porta", "ConectarAutomaticamente"}, "Descricao=?", new String[] {descricao}, null, null, null, null);
			
			if (c.getCount() > 0) {
				c.moveToFirst();
				
				edtDescricao.setText(c.getString(0));
				edtHost.setText(c.getString(1));
				edtPorta.setText(c.getString(2));
				
				if (c.getInt(3) == 1) {
					cbxConectarAutomaticamente.setChecked(true);
				} else {
					cbxConectarAutomaticamente.setChecked(false);
				}
				
			} else {
				edtDescricao.setText("");
				edtHost.setText("");
				edtPorta.setText("");
				cbxConectarAutomaticamente.setChecked(false);
			}
		} else {
			edtDescricao.setText("");
			edtHost.setText("");
			edtPorta.setText("");
			cbxConectarAutomaticamente.setChecked(false);
		}
	}

}
