let attackerId = null;
function selectPokemon(event) {
    console.log("TESTING");
    const pokemonId = event.target.getAttribute('data-pokemon-id');
    if (attackerId === null) {
        // Select attacker
        attackerId = pokemonId;
        event.target.classList.add('attacker');
    } else {
        // Attack target
        attackPokemon(attackerId, pokemonId);
        // Reset attacker selection
        attackerId = null;
        document.querySelectorAll('.card').forEach(card => card.classList.remove('attacker'));
    }
}

async function attackPokemon(attackerId, targetId) {
    try {
        const response = await fetch(`/attack/${attackerId}/${targetId}`);
        const data = await response.json();
        console.log('data :>> ', data);
        // Handle the response 
    } catch (error) {
        console.error('Error attacking Pokemon:', error);
    }
}