let matches = document.querySelectorAll("[id*=\"matches_group_\"]");

function buttonClick (group){
    let matchesClick = `matches_group_${group.value}`
    for (i = 0; i < groups.length; i++) {
        let matchesInList = matches[i];
        if (matchesInList.id == matchesClick) {
            matchesInList.className = 'showed_matches';
        } else {
            matchesInList.className = '';
        }
    }
}
