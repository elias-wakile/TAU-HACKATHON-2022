import { Image } from '@chakra-ui/react'

interface IDifficultyBoxProps {
	src: string
	onHover: () => void
	onUnHover: () => void
	onClick: () => void
}

export const DifficultyBox = ({ src, onHover, onUnHover, onClick }: IDifficultyBoxProps) => {
	return (
		<Image
			src={src}
			w='35px'
			h='100%'
			mr='1px'
			cursor='pointer'
			onMouseEnter={onHover}
			onMouseLeave={onUnHover}
			onClick={onClick}
		/>
	)
}
