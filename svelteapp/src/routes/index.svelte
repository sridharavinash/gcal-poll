<script types='ts'>
  import {onMount} from 'svelte';
  let turnout;
  let name="";
  let players=[];
  const fetchdata = (async () => {
    const response = await fetch(import.meta.env.VITE_API_URL.toString());
    return await response.json();
  })();

  function updatePlayers(){
    // if name in players array, return
    if(players.includes(name)){
      return;
    }
    // capitalize name
    name = name.charAt(0).toUpperCase() + name.slice(1);
    players = [...players, name];
  }

  onMount(async () => {
    turnout = await fetchdata;
  });
</script>

<h1>Turnout</h1>

{#if turnout}
<p>{turnout.events.name}</p>
    <ul>
      {#each players as p}
        <li>{p}</li>
      {/each}
    </ul>
    <input type="text" bind:value={name} placeholder="Enter your name" />
    <input type="button" value="Add" on:click={updatePlayers} />
{:else}
  <p>Loading...</p>

{/if}

