let timer;
let timeLeft = 10;
let quizStarted = false;

console.log("Script loaded");  // Debugging line to confirm the script is loaded

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('start-button')?.addEventListener('click', startQuiz);
    // Initially hide the timer and True/False buttons
    document.getElementById('timer').style.display = 'none';
    document.getElementById('true-button').addEventListener('click', () => checkAnswer('True'));
    document.getElementById('false-button').addEventListener('click', () => checkAnswer('False'));
});

function startQuiz() {
    if (!quizStarted) {
        quizStarted = true;
        getQuestion(); // This will fetch and display the first question
        document.getElementById('start-button').style.display = 'none';
        // Initially hide True/False buttons until the first question is fetched
        document.getElementById('true-button').style.display = 'none';
        document.getElementById('false-button').style.display = 'none';
    }
}

function getQuestion() {
    fetch('/api/get_question')
        .then(response => response.json())
        .then(data => {
            if (data.finished) {
                showFinalScore(data.score);
                // Hide buttons and timer at the end
                hideQuizElements();
            } else {
                // Show the question, timer, and buttons
                document.getElementById('question').innerText = `Question ${data.question_number} of ${data.total_questions}: ${data.question}`;
                document.getElementById('timer').style.display = 'block';
                document.getElementById('true-button').style.display = 'inline';
                document.getElementById('false-button').style.display = 'inline';
                resetTimer();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('question').innerText = 'Error fetching question.';
            hideQuizElements();
        });
}

function hideQuizElements() {
    document.getElementById('timer').style.display = 'none';
    document.getElementById('true-button').style.display = 'none';
    document.getElementById('false-button').style.display = 'none';
    document.getElementById('start-button').style.display = 'none'; // Hide start button as well
}

// ... rest of your script.js code ...


function checkAnswer(answer) {
    stopTimer();
    fetch('/api/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answer: answer }),
    })
        .then(response => response.json())
        .then(data => {
            let feedback = data.correct ? 'Correct!' : 'Wrong!';
            document.getElementById('feedback').innerText = feedback;
            document.getElementById('score').innerText = `Score: ${data.score}`;
            // Update quiz-container background color based on correctness
            let quizContainer = document.getElementById('quiz-container');
            quizContainer.style.backgroundColor = data.correct ? '#4CAF50' : '#f44336'; // Green for correct, Red for wrong
            setTimeout(() => {
                quizContainer.style.backgroundColor = ''; // Reset background color
            }, 1000); // Reset after 1 second
            getQuestion();
        })
        .catch(error => console.error('Error:', error));
}

function startTimer() {
    timeLeft = 10;
    timer = setInterval(updateTimer, 1000);
}

function updateTimer() {
    document.getElementById('timer').innerText = `Time left: ${timeLeft}`;
    timeLeft--;
    if (timeLeft < 0) {
        checkAnswer('');
    }
}

function stopTimer() {
    clearInterval(timer);
}

function resetTimer() {
    stopTimer();
    startTimer();
}


function showFinalScore(score) {
    // Save the final score to the database
    fetch('/api/finish_quiz', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            // Display the final message
            document.getElementById('question').innerText = `Congratulations! Your final score is ${score}. Thanks for taking the Quiz`;
            hideQuizElements();
            document.getElementById('feedback').innerText = '';
            // Optionally, redirect to a different page or show a link
            setTimeout(() => {
                window.location.href = '/'; // Redirect to the home page or another appropriate page
            }, 10000); // Redirect after 10 seconds
        })
        .catch(error => console.error('Error:', error));
}

