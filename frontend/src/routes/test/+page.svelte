<script>

	import Content from '$lib/content.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button/button.svelte';


	// export let data;
	let user = {};
</script>

<Meta title={user.name} description="This page displays the user profile" />

<Content>
	<!-- <Button class="secondary" on:click={async () => {}}>Logout</Button> -->
	Hello
</Content>

<style>
</style>
