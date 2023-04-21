<script>
	import Marked from '$lib/marked.svelte';
	import Content from '$lib/content.svelte';

	let md = `
\`\`\`javascript
console.log("here")
let a = 55;
// this is a comment
\`\`\`
	`;
</script>

<Marked />

<section>
	<Marked {md} />
	<textarea name="" id="" cols="30" rows="10" />
</section>

<style>
	section {
		display: flex;
	}

	textarea {
		width: 50%;
	}
</style>
