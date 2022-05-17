import { Box, BoxProps } from '@chakra-ui/react'
import { theme } from '../theme'

interface IItemDetailsProps extends BoxProps {
	title: string
	dueDate: string
}

export const ItemDetails = ({ title, dueDate, ...props }: IItemDetailsProps) => {
	return (
		<Box data-id='ItemDetails' {...props}>
			<Box fontSize={theme.fontSizes.title} color={theme.defaultColor} w='100%'>
				{title}
			</Box>
			<Box marginTop='15px' fontSize={theme.fontSizes.medium} color={theme.defaultColor} w='100%'>
				{`Due Date: ${dueDate}`}
			</Box>
		</Box>
	)
}
