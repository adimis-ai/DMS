<script>
  import { onMount } from 'svelte';
  import Loader from "$lib/components/Loader.svelte"
  let files = [];
  let loader = false;

  async function fetchFiles() {
    loader = true
    try {
      const response = await fetch("http://127.0.0.1:8000/get_files/", {
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      loader = false
      files = data.files;
    } catch (error) {
      console.error(error);
    }
  }

  async function deleteFile(file_id) {
    loader = true
    try {
      await fetch(`http://127.0.0.1:8000/delete_files/${file_id}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      await fetchFiles();
      loader = false
    } catch (error) {
      console.error(error);
    }
  }

  async function downloadFile(file_id) {
    loader = true
    try {
      window.location.href = `http://127.0.0.1:8000/get_files/${file_id}/`;
      loader = false
    } catch (error) {
      console.error(error);
    }
  }
  onMount(fetchFiles);
</script>


{#if loader==true}
  <Loader/>
{/if}
{#if loader == false}
  {#if files.length > 0}
    <ul>
      {#each files as file}
        <li>
          <button class="btn mx-3 my-3" on:click={() => deleteFile(file[0])}>Delete</button>
          <button class="btn mx-3 my-3" on:click={() => downloadFile(file[0])}>Download</button>
          {file[1]} 
        </li>
      {/each}
    </ul>
  {/if}
{/if}