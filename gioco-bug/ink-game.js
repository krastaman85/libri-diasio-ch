const SAVE_KEY = 'diasio-bug-episode-01-ink-v1';
const sceneDetails = {
  garage: { location: 'Residenza Meridiana · piano -2', title: 'Il garage', time: '07:14', mark: '-02' },
  assembly: { location: 'Residenza Meridiana · sala comune', title: 'Aggiornamento obbligatorio', time: '19:00', mark: '19:41' }
};

const log = document.querySelector('#story-log');
const choicesElement = document.querySelector('#story-choices');
const statusElement = document.querySelector('#engine-status');
const clueList = document.querySelector('#clue-list');
let story;
let clues = [];
let transcript = [];
let currentScene = '';
let currentStep = 1;

function saveStory() {
  try {
    localStorage.setItem(SAVE_KEY, JSON.stringify({ story: story.state.ToJson(), clues, transcript, currentScene, currentStep }));
    document.querySelector('#save-note').textContent = 'Progressi salvati su questo dispositivo.';
  } catch {
    document.querySelector('#save-note').textContent = 'Il salvataggio locale non è disponibile in questo browser.';
  }
}

function renderClues() {
  clueList.replaceChildren();
  if (clues.length === 0) {
    const empty = document.createElement('li');
    empty.className = 'empty-state';
    empty.textContent = 'Gli indizi compariranno qui.';
    clueList.append(empty);
  } else {
    clues.forEach(clue => {
      const item = document.createElement('li');
      item.textContent = clue;
      clueList.append(item);
    });
  }
  document.querySelector('#clue-count').textContent = `${clues.length} ${clues.length === 1 ? 'INDIZIO' : 'INDIZI'}`;
}

function renderScene() {
  const scene = sceneDetails[currentScene];
  if (!scene) return;
  document.querySelector('#scene-location').textContent = scene.location;
  document.querySelector('#scene-title').textContent = scene.title;
  document.querySelector('#scene-clock').textContent = scene.time;
  document.querySelector('#scene-time').textContent = scene.time;
  document.querySelector('#scene-mark').textContent = scene.mark;
  const art = document.querySelector('#scene-art');
  art.dataset.space = currentScene;
  art.setAttribute('aria-label', `Scena illustrata: ${scene.location}`);
  const stepText = currentStep >= 3 ? 'GIORNO 15 · 3 / 3' : `GIORNO 11 · ${currentStep} / 3`;
  document.querySelector('#progress-label').textContent = stepText;
  const progress = document.querySelector('.progress-track');
  progress.setAttribute('aria-valuenow', String(Math.min(currentStep, 3)));
  document.querySelector('#progress-fill').style.width = `${Math.min(currentStep, 3) / 3 * 100}%`;
}

function processTags(tags) {
  for (const tag of tags) {
    const separator = tag.indexOf(':');
    if (separator < 0) continue;
    const name = tag.slice(0, separator).trim();
    const value = tag.slice(separator + 1).trim();
    if (name === 'scene' && value !== currentScene) {
      currentScene = value;
      renderScene();
    } else if (name === 'step') {
      currentStep = Number(value) || currentStep;
      renderScene();
    } else if (name === 'clue' && value && !clues.includes(value)) {
      clues.push(value);
      renderClues();
    } else if (name === 'ending') markComplete();
  }
}

function markComplete() {
  document.querySelector('#scene-status').textContent = 'PUNTATA COMPLETATA';
  document.querySelector('#scene-status').classList.add('open');
  statusElement.textContent = 'Puntata completata.';
  statusElement.classList.add('complete');
}

function appendPassage(text, record = true) {
  if (record) transcript.push(text);
  const passage = document.createElement('p');
  passage.className = 'story-passage';
  passage.textContent = text;
  log.append(passage);
}

function showChoices() {
  choicesElement.replaceChildren();
  story.currentChoices.forEach((choice, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'story-choice';
    button.textContent = choice.text;
    button.addEventListener('click', () => {
      story.ChooseChoiceIndex(index);
      appendPassage(choice.text);
      continueStory();
    }, { once: true });
    choicesElement.append(button);
  });
}

function continueStory() {
  choicesElement.replaceChildren();
  while (story.canContinue) {
    const text = story.Continue().trim();
    processTags(story.currentTags || []);
    if (text) appendPassage(text);
  }
  if (story.currentChoices.length) showChoices();
  else if (!story.canContinue) markComplete();
  saveStory();
  log.scrollTop = log.scrollHeight;
}

async function startGame() {
  try {
    if (!window.inkjs || !window.inkjs.Compiler) throw new Error('Il motore narrativo non è disponibile.');
    statusElement.textContent = 'Caricamento della Puntata 1…';
    const response = await fetch('/gioco-bug/episode-01.ink', { cache: 'no-cache' });
    if (!response.ok) throw new Error('Non è stato possibile caricare la storia.');
    const source = await response.text();
    const compiler = new window.inkjs.Compiler(source);
    story = compiler.Compile();
    if (!story) throw new Error('La storia non è stata compilata.');

    try {
      const saved = JSON.parse(localStorage.getItem(SAVE_KEY));
      if (saved && saved.story) {
        story.state.LoadJson(saved.story);
        clues = Array.isArray(saved.clues) ? saved.clues : [];
        transcript = Array.isArray(saved.transcript) ? saved.transcript : [];
        currentScene = typeof saved.currentScene === 'string' ? saved.currentScene : '';
        currentStep = Number(saved.currentStep) || 1;
        transcript.forEach(text => appendPassage(text, false));
      }
    } catch {}

    renderClues();
    renderScene();
    document.querySelector('#scene-status').textContent = 'IN CORSO';
    statusElement.textContent = 'Storia pronta.';
    statusElement.classList.add('complete');
    if (!story.canContinue && story.currentChoices.length === 0) markComplete();
    continueStory();
  } catch (error) {
    statusElement.textContent = `${error.message} Ricarica la pagina per riprovare.`;
    statusElement.classList.add('error');
  }
}

function resetGame() {
  try {
    localStorage.removeItem(SAVE_KEY);
  } catch {}
  window.location.reload();
}

document.querySelector('#reset-game').addEventListener('click', resetGame);
startGame();
