function validScore(event){
    const mathScore = parseFloat(document.getElementById("math_score").value);
    const physScore = parseFloat(document.getElementById("physics_score").value);
    const inforScore = parseFloat(document.getElementById("informatics_score").value);

    if (
        mathScore >= 0 && mathScore <= 20 &&
        physScore >= 0 && physScore <= 20 &&
        inforScore >= 0 && inforScore <= 20
    ){
        alert("Valid");
        return true;
    }
    else{
        alert("INVALID SCORE");
        return false;
    }
}