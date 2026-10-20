
const API = "/api";

let loggedInAccount = null;

const mainSections = [
    "mainMenu",
    "createSection",
    "loginSection",
    "accountSection"
];

function showSection(sectionId) {
    mainSections.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.style.display = id === sectionId ? "block" : "none";
        }
    });

    hideOperations();
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function hideOperations() {
    ["depositSection", "withdrawSection"].forEach(id => {
        const element = document.getElementById(id);
        if (element) element.style.display = "none";
    });
}

function setMessage(id, message, success = false) {
    const element = document.getElementById(id);
    if (!element) return;

    element.textContent = message;
    element.style.color = success ? "#16864b" : "#c62828";
}

function clearMessages() {
    [
        "createResult",
        "loginResult",
        "depositResult",
        "withdrawResult",
        "operationResult"
    ].forEach(id => setMessage(id, ""));
}

function showCreate() {
    clearMessages();
    showSection("createSection");
}

function showLogin() {
    clearMessages();
    showSection("loginSection");
}

function goHome() {
    clearMessages();
    showSection("mainMenu");
}

function showDeposit() {
    if (!loggedInAccount) {
        showLogin();
        setMessage("loginResult", "Please log in first.");
        return;
    }

    hideOperations();
    document.getElementById("depositSection").style.display = "block";
}

function showWithdraw() {
    if (!loggedInAccount) {
        showLogin();
        setMessage("loginResult", "Please log in first.");
        return;
    }

    hideOperations();
    document.getElementById("withdrawSection").style.display = "block";
}

async function apiRequest(path, options = {}) {
    const response = await fetch(`${API}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || "The request failed.");
    }

    return data;
}

function updateAccountUI(data) {
    loggedInAccount = String(data.accountNumber);

    const welcome = document.getElementById("welcome");
    const accountNumber = document.getElementById("loggedAccount");
    const balance = document.getElementById("currentBalance");
    const dashboardBalance = document.getElementById("dashboardBalance");

    if (welcome) welcome.textContent = `Welcome, ${data.name}!`;
    if (accountNumber) accountNumber.textContent = loggedInAccount;

    if (balance) {
        balance.textContent = Number(data.balance).toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    if (dashboardBalance) {
        dashboardBalance.textContent = Number(data.balance).toLocaleString("en-IN", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }

    showSection("accountSection");
}

async function createAccount() {
    const name = document.getElementById("name").value.trim();
    const accountType = document.getElementById("accountType").value;
    const initialBalance = document.getElementById("initialBalance").value;

    if (!name) {
        setMessage("createResult", "Please enter your name.");
        return;
    }

    if (initialBalance.trim() === "" ||
        !Number.isFinite(Number(initialBalance)) ||
        Number(initialBalance) < 0) {
        setMessage("createResult", "Enter a valid initial balance.");
        return;
    }

    try {
        const data = await apiRequest("/accounts", {
            method: "POST",
            body: JSON.stringify({ name, accountType, initialBalance })
        });

        setMessage(
            "createResult",
            `Account created! Your account number is ${data.accountNumber}. Please save it and log in.`,
            true
        );

        document.getElementById("accountNumber").value = data.accountNumber;
        document.getElementById("name").value = "";
        document.getElementById("initialBalance").value = "";
    } catch (error) {
        setMessage("createResult", error.message);
    }
}

async function login() {
    const accountNumber =
        document.getElementById("accountNumber").value.trim();

    if (!accountNumber) {
        setMessage("loginResult", "Please enter your account number.");
        return;
    }

    try {
        const data = await apiRequest("/login", {
            method: "POST",
            body: JSON.stringify({ accountNumber })
        });

        updateAccountUI(data);
        clearMessages();
    } catch (error) {
        setMessage("loginResult", error.message);
    }
}

async function refreshAccount() {
    if (!loggedInAccount) return;

    const data = await apiRequest(
        `/accounts/${encodeURIComponent(loggedInAccount)}`
    );

    updateAccountUI(data);
}

async function depositMoney() {
    if (!loggedInAccount) {
        showLogin();
        return;
    }

    const input = document.getElementById("depositAmount");
    const amount = Number(input.value);

    if (input.value.trim() === "" ||
        !Number.isFinite(amount) || amount <= 0) {
        setMessage("depositResult", "Enter an amount greater than zero.");
        return;
    }

    try {
        const data = await apiRequest(
            `/accounts/${encodeURIComponent(loggedInAccount)}/deposit`,
            {
                method: "POST",
                body: JSON.stringify({ amount })
            }
        );

        setMessage("depositResult", data.message, true);
        input.value = "";
        await refreshAccount();
    } catch (error) {
        setMessage("depositResult", error.message);
    }
}

async function withdrawMoney() {
    if (!loggedInAccount) {
        showLogin();
        return;
    }

    const input = document.getElementById("withdrawAmount");
    const amount = Number(input.value);

    if (input.value.trim() === "" ||
        !Number.isFinite(amount) || amount <= 0) {
        setMessage("withdrawResult", "Enter an amount greater than zero.");
        return;
    }

    try {
        const data = await apiRequest(
            `/accounts/${encodeURIComponent(loggedInAccount)}/withdraw`,
            {
                method: "POST",
                body: JSON.stringify({ amount })
            }
        );

        setMessage("withdrawResult", data.message, true);
        input.value = "";
        await refreshAccount();
    } catch (error) {
        setMessage("withdrawResult", error.message);
    }
}

async function checkBalance() {
    if (!loggedInAccount) {
        showLogin();
        setMessage("loginResult", "Please log in first.");
        return;
    }

    try {
        await refreshAccount();
        setMessage(
            "operationResult",
            "Your balance has been updated.",
            true
        );
    } catch (error) {
        setMessage("operationResult", error.message);
    }
}

async function calculateInterest() {
    if (!loggedInAccount) {
        showLogin();
        setMessage("loginResult", "Please log in first.");
        return;
    }

    try {
        const data = await apiRequest(
            `/accounts/${encodeURIComponent(loggedInAccount)}/interest`
        );

        await refreshAccount();

        setMessage(
            "operationResult",
            `Interest added: ₹${Number(data.interestAdded).toFixed(2)}. Updated balance: ₹${Number(data.balance).toFixed(2)}.`,
            true
        );
    } catch (error) {
        setMessage("operationResult", error.message);
    }
}

function logout() {
    loggedInAccount = null;
    clearMessages();
    showSection("mainMenu");
}

function exitApp() {
    logout();
}

document.addEventListener("DOMContentLoaded", () => {
    showSection("mainMenu");
});
