<script>
  import { onMount } from "svelte";
  import { fly } from "svelte/transition";

  const dictPath = "/dict.json";
  let dict;
  let letters = "";
  let length = -1;
  $: generated = [...generate(letters, length)];

  onMount(async () => {
    console.log("the component has mounted");
    const resp = await fetch(dictPath);
    dict = await resp.json();
  });

  function convertStrToObj(str) {
    let obj = {};
    for (const c of str) obj[c] = (obj[c] || 0) + 1;
    return obj;
  }

  function* generate(letters, length) {
    letters = convertStrToObj(letters.toLowerCase());

    function* traverse(cur, letters, word) {
      if (!cur) return;
      if (cur["word"] && (length === -1 || word.length === length))
        yield word.join("");

      for (const c in letters) {
        if (letters[c] === 0) continue;

        letters[c]--;
        word.push(c);
        yield* traverse(cur[c], letters, word);
        word.pop();
        letters[c]++;
      }
    }

    yield* traverse(dict, letters, []);
  }
</script>


{#if !dict}
<p>fetching database...</p>
{/if}

<input type="text" bind:value="{letters}" />
<input type="number" bind:value="{length}" />

<ul>
{#each generated as word}
  <li in:fly>{word}</li>
{/each}
</ul>
