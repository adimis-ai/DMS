<script>
    import Loader from "$lib/components/Loader.svelte"
    let query = "";
    let loader = false
    let searchResults = [];
  
    async function handleSearch() {
        try {
            loader = true
            const response = await fetch(`http://127.0.0.1:8000/search/?query=${query}`, {
            method: "POST",
            headers: {
                "Accept": "application/json"
            }
            });
            const data = await response.json();
            loader = false
            searchResults = data.files;
        } catch (error) {
            console.error(error);
        }
    }
</script>
  

{#if loader==true}
	<Loader/>
{/if}
{#if loader==false}
    <div class="mx-3">
        <div class="form-control">
            <div class="input-group">
                <input type="text" placeholder="Search…" class="input input-bordered" bind:value={query} />
                <button class="btn btn-square" on:click={handleSearch}>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                </button>
            </div>
        </div>
        {#if searchResults.length > 0}
            <ul>
            {#each searchResults as file}
                <li>
                    {file.file_name}
                </li>
            {/each}
            </ul>
        {/if}
    </div>
{/if}
  