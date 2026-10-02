VAR phone_seen = false
VAR door_seen = false
VAR agenda_seen = false
VAR release_seen = false
VAR cesare_seen = false
VAR reaction_seen = false
VAR post_seen = false
VAR removal_seen = false

-> garage

=== garage ===
# scene:garage
# step:1
# time:07:14
Il garage di Residenza Meridiana odora di cera per pavimenti anche al piano meno due. Nadia abita lì da undici giorni. Ogni mattina, alle 7:14, il telefono si accende da solo.

-> garage_hub

=== garage_hub ===
{not phone_seen:
Il display azzurro di Meridiana Life è acceso.
- else:
Il telefono è ancora acceso. L’ultima sincronizzazione registrata è alle 07:14.
}
{not door_seen:
In fondo alla rampa c’è la porta blindata senza targhetta, tra i box privati.
- else:
La porta tecnica è sempre chiusa. Yusuf disse che solo l’amministrazione ha accesso agli impianti.
}
* {not phone_seen} [Esamina il telefono] -> phone
* {not door_seen} [Ricorda la porta degli impianti] -> door
* [Raggiungi la sala comune per l’assemblea delle diciannove] -> meeting

=== phone ===
Alle 7:14, un minuto prima della sveglia che Nadia non ha ancora impostato, lo schermo si accende. Meridiana Life: l’app apre il cancello, prenota la palestra e manda le notifiche dei pacchi.
# clue:Ogni mattina il telefono di Nadia si accende alle 07:14.
~ phone_seen = true
-> garage_hub

=== door ===
Durante il trasloco, Nadia chiese a Yusuf se la porta blindata fosse un ripostiglio. Lui rispose: «Impianti tecnici. Non è nell’elenco degli spazi condominiali. Non ne ha accesso nessuno, a parte l’amministrazione.»
# clue:La porta senza targhetta dà accesso agli impianti; la gestisce l’amministrazione.
~ door_seen = true
-> garage_hub

=== meeting ===
# scene:assembly
# step:2
# time:19:00
Alle diciannove, la sala comune è quasi piena. Nadia si siede in fondo e osserva. All’ordine del giorno, tra il tetto e le piante del cortile, c’è una riga: aggiornamento tecnico di Meridiana Life, approvazione formale.

Cesare Rocchi Molteni, presidente da otto anni, dice che il punto quattro è una formalità. Propone di approvare l’aggiornamento per acclamazione, senza leggere le note di rilascio.

-> meeting_hub

=== meeting_hub ===
{not agenda_seen:
L’ordine del giorno riduce l’aggiornamento a una formalità.
- else:
La voce sull’aggiornamento è ancora lì, tra due lavori condominiali ordinari.
}
{not release_seen:
Nessuno ha letto le note di rilascio.
- else:
Le note non sono state lette prima dell’approvazione.
}
{not cesare_seen:
Cesare passa al preventivo B per il rifacimento del tetto e dice di non avere interessi personali.
- else:
Cesare ha negato qualsiasi interesse personale nel preventivo che sta sostenendo.
}
* {not agenda_seen} [Esamina l’ordine del giorno] -> agenda
* {not release_seen} [Controlla se qualcuno ha letto le note] -> release_notes
* {not cesare_seen} [Ascolta Cesare mentre parla del preventivo B] -> cesare
* {agenda_seen and release_seen and cesare_seen} [Ricostruisci la sequenza] -> deduce_update

=== agenda ===
Il punto quattro è una formalità: «aggiornamento tecnico Meridiana Life, approvazione formale». Compare tra il rifacimento del tetto e la sostituzione delle piante del cortile.
# clue:L’aggiornamento dell’app viene messo ai voti come una formalità.
~ agenda_seen = true
-> meeting_hub

=== release_notes ===
Nessuno chiede di leggere le note. I residenti annuiscono mentre Cesare propone di approvare l’aggiornamento per acclamazione.
# clue:L’assemblea approva l’aggiornamento senza leggere le note di rilascio.
~ release_seen = true
-> meeting_hub

=== cesare ===
Cesare sostiene il preventivo B e afferma di non avere interessi personali. Poco dopo, il suo telefono vibra; lui lo guarda per un istante e lo rimette in tasca.
# clue:Il telefono di Cesare vibra subito dopo la sua dichiarazione sul preventivo B.
~ cesare_seen = true
-> meeting_hub

=== deduce_update ===
Le note non sono state lette. L’aggiornamento è appena stato approvato. Cesare ha detto di non avere interessi personali sul preventivo B.

Quale ipotesi è sostenuta fin qui dagli indizi?
+ [L’aggiornamento è entrato in funzione dopo l’approvazione, ma non sai ancora cosa faccia.] -> correct_update
+ [Il telefono di Cesare ha vibrato per confermare che il preventivo è regolare.] -> wrong_update
+ [Nadia ha già la prova che il portiere ha scritto il software.] -> wrong_update

=== wrong_update ===
Questa conclusione va oltre ciò che gli indizi dimostrano. Non sai chi abbia creato l’app né perché il telefono di Cesare abbia vibrato.
-> deduce_update

=== correct_update ===
# clue:L’aggiornamento è stato approvato, ma autore e funzione del sistema restano da accertare.
# step:3
Tutti i telefoni vibrano insieme. Sullo schermo compare: «Meridiana Life si è aggiornata. Benvenuti in Trasparenza Meridiana.»

Poco dopo, Cesare sostiene il preventivo B e dichiara di non avere interessi personali. Il suo telefono vibra da solo. La bacheca si aggiorna con un post senza nome, alle 19:41:

«Il preventivo B è di mio cognato. Se lo dico gli altri capiscono e mi tolgono la presidenza. Devo dirlo onesto, sembra più credibile.»

-> post_hub

=== post_hub ===
* [Esamina il post anonimo] -> post
* {not reaction_seen} [Osserva le reazioni nella sala] -> reactions
* {not removal_seen} [Prova a rimuovere il post] -> removal
* {post_seen and reaction_seen and removal_seen} [Deduce come funziona la trasparenza] -> deduce_mechanism

=== post ===
Il post mostra un’icona grigia al posto del nome e l’orario 19:41. È visibile sulla bacheca condominiale, aperta sui telefoni per il voto.
# clue:Alle 19:41 la bacheca mostra senza nome il pensiero di Cesare sul preventivo B.
~ post_seen = true
-> post_hub

=== reactions ===
Ines Bettarini guarda Cesare e il telefono due volte. Sara Weiss resta immobile, come se osservasse un sintomo. Giulio Nervi ride troppo forte, e si vede che ha paura.
# clue:Ines, Sara e Giulio reagiscono alla rivelazione in modi diversi; Nadia nota che hanno capito qualcosa.
~ reaction_seen = true
-> post_hub

=== removal ===
Nadia tiene premuto sul post. Non compare alcuna opzione per eliminarlo. Sotto il messaggio legge: «Trasparenza Meridiana non può essere rimossa da un singolo utente. Contattare l’amministrazione per la disattivazione collettiva.»
# clue:Un singolo residente non può rimuovere il post; la disattivazione spetta all’amministrazione collettiva.
~ removal_seen = true
-> post_hub

=== deduce_mechanism ===
Ora hai il post, la sequenza delle azioni di Cesare e le reazioni nella sala. Che cosa dimostrano?
+ [L’app rende pubblici i pensieri di chi mente ad alta voce.] -> correct_mechanism
+ [L’app pubblica a caso i pensieri dei residenti.] -> wrong_mechanism
+ [Il post prova che tutti i residenti hanno mentito.] -> wrong_mechanism

=== wrong_mechanism ===
La conclusione non spiega la sequenza osservata: la confessione di Cesare appare dopo la sua dichiarazione sul preventivo B. Rivedi le prove.
-> deduce_mechanism

=== correct_mechanism ===
# clue:La confessione di Cesare compare subito dopo la bugia detta ad alta voce.
L’app non ha rivelato un segreto casuale. Ha pubblicato il pensiero non filtrato di Cesare dopo che lui ha negato il proprio interesse.

-> deduce_reactions

=== deduce_reactions ===
Che cosa puoi concludere sulle tre persone che hanno reagito?
+ [Le loro reazioni mostrano che hanno capito qualcosa, ma non provano cosa sapessero prima.] -> correct_reactions
+ [Ines, Sara e Giulio hanno certamente creato l’app insieme.] -> wrong_reactions
+ [Le reazioni provano che il post è falso.] -> wrong_reactions

=== wrong_reactions ===
Le espressioni dei residenti non bastano a dimostrare chi abbia creato il sistema o cosa sapesse in precedenza.
-> deduce_reactions

=== correct_reactions ===
# clue:Le reazioni suggeriscono riconoscimento, non identificano chi abbia creato o attivato il sistema.
Nadia prova a tenere premuto sul post. Nessuna opzione di eliminazione: la disattivazione deve essere collettiva. Cesare, che ha appena minimizzato l’accaduto, è anche il presidente dell’assemblea.

Quella notte Nadia apre un file di appunti. Registra la data, l’aggiornamento, la confessione comparsa sulla bacheca e le reazioni che ha osservato.

La domanda che lascia in fondo alla pagina non ha risposta: chi, nel palazzo, sa già cosa accadrà agli altri?
# step:3
# ending:episode-1
-> END
