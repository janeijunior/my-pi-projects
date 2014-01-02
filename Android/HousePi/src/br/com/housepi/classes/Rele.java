package br.com.housepi.classes;
import java.io.Reader;
import java.io.StringReader;
import java.util.Iterator;
import java.util.List;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;
import android.widget.ToggleButton;
import br.com.housepi.classes.Conexao;

public class Rele {
	private Integer status;
	private Integer numero;
	private String nome;
	private ToggleButton botao;
	
	public Rele(Integer numero, ToggleButton botao) {
		super();
		this.numero = numero;
		this.botao = botao;
	}

	public Rele(Integer numero) {
		super();
		this.numero = numero;
	}

	public Integer getStatus() {
	    
		return status;
	}

	public ToggleButton getBotao() {
		return botao;
	}

	public void setBotao(ToggleButton botao) {
		this.botao = botao;
	}

	public void setStatus(Integer status) {
		this.status = status;
	}

	public Integer getNumero() {
		return numero;
	}

	public void setNumero(Integer numero) {
		this.numero = numero;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}	
	
	public Boolean ligar() {
		return montarEnviarXMLControle("Ligar");
	}
	
	public Boolean desligar() {
		return montarEnviarXMLControle("Desliga");
	}
	
	private Boolean montarEnviarXMLControle(String comando) {
		Document doc = new Document();
		Element root = new Element("Rele");
		       
		Element acao = new Element("Acao");
		acao.setText(comando);
		root.addContent(acao);
		
		Element numero = new Element("Numero");
		numero.setText(getNumero().toString());
		root.addContent(numero);
		doc.setRootElement(root);
		
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		if (Conexao.receberRetornoStatic().equals("Ok")) {
			return true;
		} else {
			return false;
		}
	}
	
	public static List<Rele> getConfiguracaoStatus(List<Rele> listaReles) {
		try {
			Document doc = new Document();
			Element root = new Element("StatusRele");
			doc.setRootElement(root);

			//Format format = Format.getPrettyFormat();
	        //format.setEncoding("ISO-8859-1");
	        														//format	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

			String mensagem = "";

			mensagem = Conexao.receberRetornoStatic();
						
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);

			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}

			Element retorno = (Element) doc.getRootElement();
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();

			for (Rele rele : listaReles) {
				Element element = (Element) j.next();
		
				rele.setStatus(element.getAttribute("Status").getIntValue());
				rele.setNome(element.getAttribute("Nome").getValue());

				if (rele.getBotao() != null) {
					rele.getBotao().setChecked(rele.getStatus() == 1);
					rele.getBotao().setText(rele.getNome());
					rele.getBotao().setTextOn(rele.getNome());
					rele.getBotao().setTextOff(rele.getNome());
				}
			}
		
		return listaReles;
		
		} catch (Exception e) {
			return listaReles;
		}
	}
}
