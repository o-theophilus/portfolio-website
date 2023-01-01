<script>
	import { page } from '$app/stores';

	export let title;
	export let description;
	export let image;

	let imageAlt = image;
	let url = `https://theophilus.website${$page.url.pathname}`;
	let type = 'website';
	let twitterCard = 'summary_large_image';
</script>

<svelte:head>
	{#if title}
		<title>{title}</title>
		<meta name="title" content={title} />
		<meta property="og:title" content={title} />
		<meta property="twitter:title" content={title} />
	{/if}

	{#if description}
		<meta name="description" content={description} />
		<meta property="og:description" content={description} />
		<meta property="twitter:description" content={description} />
	{/if}

	{#if image}
		<meta property="og:image" content="/images/{image}" />
		<meta property="twitter:image" content="/images/{image}" />
	{/if}

	{#if imageAlt}
		<meta property="og:image:alt" content={imageAlt} />
		<meta property="twitter:image:alt" content={imageAlt} />
	{/if}

	{#if url}
		<meta property="og:url" content={url} />
		<meta property="twitter:url" content={url} />
	{/if}

	{#if type}
		<meta property="og:type" content={type} />
	{/if}

	<meta property="twitter:card" content={twitterCard} />
</svelte:head>
