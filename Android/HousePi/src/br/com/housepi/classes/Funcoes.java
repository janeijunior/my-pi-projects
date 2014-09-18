package br.com.housepi.classes;

import java.text.SimpleDateFormat;
import java.util.Date;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.preference.PreferenceManager;
import android.widget.Toast;

@SuppressLint({ "SimpleDateFormat"})
public class Funcoes {
	private static final String dataBanco = "yyyy-MM-dd HH:mm:ss";
	private static final String dataLocal = "dd/MM/yyyy HH:mm:ss";	
	
	public static void salvarDadosComponente(String key, String value, Context classe) {
        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(classe);
        Editor editor = sharedPreferences.edit();
        editor.putString(key, value);
        editor.commit();
	}
	
	public static String carregarDadosComponente(String key, String value, Context classe) {
		SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(classe);
		return sharedPreferences.getString(key, value);       
	}	
		
	public static String formatarDataHoraBanco(Date dataHora) {
		return new SimpleDateFormat(dataBanco).format(dataHora);  
	}
	
	public static String formatarDataHoraLocal(Date dataHora) {
		return new SimpleDateFormat(dataLocal).format(dataHora);  
	}
	
	public static Date formatarDataHora(String dataHora) {
		try {
			return new SimpleDateFormat(dataBanco).parse(dataHora);  
		} catch (Exception ex) {
			ex.printStackTrace();
			return null;
		}
	}
	
	@SuppressWarnings("deprecation")
	public static void msgDialogoInformacao(String titulo, String mensagem, Context classe) {
		AlertDialog alertDialog = new AlertDialog.Builder(classe).create();
		alertDialog.setTitle(titulo);
		alertDialog.setMessage(mensagem);
		alertDialog.setButton("OK", new DialogInterface.OnClickListener() {
			public void onClick(DialogInterface dialog, int which) {
		
			}
		});
		//alertDialog.setIcon(R.drawable.informacao);
		alertDialog.show();
	}
	
	public static void msgToastErroComando(Context classe) {
		Toast.makeText(classe, "Não foi possível enviar o comando.", Toast.LENGTH_SHORT).show();
	}
	
	public static void msgToastDadosGravados(Context classe) {
		Toast.makeText(classe, "Dados gravados com sucesso!", Toast.LENGTH_SHORT).show();
	}
	
	public static void msgToastErroGravar(Context classe) {
		Toast.makeText(classe, "Não foi possível gravar os dados no servidor.", Toast.LENGTH_SHORT).show();
	}
	
	/*public static String removerAcentos(String str) {  
		str = Normalizer.normalize(str, Normalizer.Form.NFD);
		str = str.replaceAll("[^\\p{ASCII}]", "");
		return str;
	}*/ 
}
