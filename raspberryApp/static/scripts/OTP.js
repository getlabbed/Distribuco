//Code fait entièrement par chatGPT

const intervalDuration = 60;

async function getOtpCode() {
  const response = await fetch('/get-otp-code');
  const data = await response.json();
  return data.otp_code;
}

function getTimeRemaining() {
  const currentTime = Math.floor(Date.now() / 1000);
  const timeElapsed = currentTime % intervalDuration;
  const timeRemaining = intervalDuration - timeElapsed;
  return timeRemaining;
}

async function updateOtpDisplay() {
  const otpDisplay = document.getElementById('otp-display');
  const otpCode = await getOtpCode();
  otpDisplay.innerText = otpCode;
}

function startCountdown() {
  let counter = getTimeRemaining();
  const secondsCounter = document.getElementById('seconds-counter');
  secondsCounter.innerText = counter;
  updateOtpDisplay();

  const countdown = setInterval(async () => {
    counter--;

    if (counter < 0) {
      counter = intervalDuration;
      await updateOtpDisplay();
    }

    secondsCounter.innerText = counter;
  }, 1000);
}

startCountdown();