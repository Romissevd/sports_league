let groups = document.querySelectorAll("[id*=\"group \"]");
let matches = document.querySelectorAll("[id*=\"matches_group_\"]");

function buttonClick (group){
    let groupClick = `group ${group.value}`;
    let matchesClick = `matches_group_${group.value}`;
    for (i = 0; i < groups.length; i++) {
        let groupInList = groups[i];
        let matchesInList = matches[i];
        if (groupInList.id == groupClick) {
            groupInList.className = 'showed';
        } else {
            groupInList.className = '';
        }
        if (matchesInList.id == matchesClick) {
            matchesInList.className = 'showed_matches';
        } else {
            matchesInList.className = '';
        }
    }
}
