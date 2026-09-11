let loggedAccount = null;


// Show Create Account
function showCreate() {
    document.getElementById("mainMenu").style.display = "none";
    document.getElementById("createSection").style.display = "block";
}


// Show Login
function showLogin() {
    document.getElementById("mainMenu").style.display = "none";
    document.getElementById("loginSection").style.display = "block";
}


// Go Home
function goHome() {
    document.getElementById("createSection").style.display = "none";
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("accountSection").style.display = "none";
    document.getElementById("mainMenu").style.display = "block";
}


// Create Account
async function createAccount() {

    const name = document.getElementById("name").value;
    const accountType = document.getElementById("accountType").value;
    const balance = document.getElementById("initialBalance").value;

    const response = await fetch("/create-account", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            account_type: accountType,
            balance: balance
        })
    });

    const data = await response.json();

    document.getElementById("createResult").innerText =
        data.message || data.error;

    if (data.account_number) {
        document.getElementById("createResult").innerText =
            `Account created successfully! Your account number is ${data.account_number}`;
    }
}


// Login
async function login() {

    const accountNumber =
        document.getElementById("accountNumber").value;

    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            account_number: accountNumber
        })
    });

    const data = await response.json();

    if (data.error) {
        document.getElementById("loginResult").innerText =
            data.error;
        return;
    }

    loggedAccount = data.account_number;

    document.getElementById("loginSection").style.display = "none";
    document.getElementById("accountSection").style.display = "block";

    document.getElementById("welcome").innerText =
        `Welcome, ${data.name}`;

    document.getElementById("loggedAccount").innerText =
        data.account_number;

    document.getElementById("currentBalance").innerText =
        data.balance;
}


// Show Deposit
function showDeposit() {

    document.getElementById("depositSection").style.display = "block";
    document.getElementById("withdrawSection").style.display = "none";
}


// Deposit Money
async function depositMoney() {

    const amount =
        document.getElementById("depositAmount").value;

    const response = await fetch("/deposit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            account_number: loggedAccount,
            amount: amount
        })
    });

    const data = await response.json();

    document.getElementById("depositResult").innerText =
        data.message || data.error;

    if (data.balance !== undefined) {
        document.getElementById("currentBalance").innerText =
            data.balance;
    }
}


// Show Withdraw
function showWithdraw() {

    document.getElementById("withdrawSection").style.display = "block";
    document.getElementById("depositSection").style.display = "none";
}


// Withdraw Money
async function withdrawMoney() {

    const amount =
        document.getElementById("withdrawAmount").value;

    const response = await fetch("/withdraw", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            account_number: loggedAccount,
            amount: amount
        })
    });

    const data = await response.json();

    document.getElementById("withdrawResult").innerText =
        data.message || data.error;

    if (data.balance !== undefined) {
        document.getElementById("currentBalance").innerText =
            data.balance;
    }
}


// Check Balance
async function checkBalance() {

    const response =
        await fetch(`/balance/${loggedAccount}`);

    const data = await response.json();

    if (data.balance !== undefined) {

        document.getElementById("currentBalance").innerText =
            data.balance;

        document.getElementById("operationResult").innerText =
            `Current balance: ₹${data.balance}`;
    }
}


// Calculate Interest
async function calculateInterest() {

    const response =
        await fetch(`/interest/${loggedAccount}`);

    const data = await response.json();

    document.getElementById("operationResult").innerText =
        data.message
        ? `Interest: ₹${data.interest}`
        : data.error;
}


// Logout
function logout() {

    loggedAccount = null;

    document.getElementById("accountSection").style.display = "none";

    document.getElementById("depositSection").style.display = "none";
    document.getElementById("withdrawSection").style.display = "none";

    document.getElementById("mainMenu").style.display = "block";
}


// Exit
function exitApp() {

    document.body.innerHTML = `
        <div class="container">
            <h1>Thank you for using our Bank!</h1>
            <p>You have exited the application.</p>
        </div>
    `;
}